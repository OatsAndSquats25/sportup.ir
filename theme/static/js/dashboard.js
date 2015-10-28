(function () {

	//=======================================

	dashboard = {
		init : function () {
			self = this;
			this.clubID = CLUBS[0].id;
			this.flagModifySessionList = 0;
			this.week = 0;
			this.router();
			this.bindEvents();
			this.clubOwnerID = clubOwnerID;

            setInterval(function(){
                if (self.isSession){
                	self.getSessions(self.week);
					self.sessionAttendanceList();
                }
            }, 500000);

			$.ajaxSetup({
				cache : false,
				beforeSend : function() {
					$('#overlay').fadeIn(100);
					$('#loading').css('top', '10px');
				},
				complete : function() {
					$('#overlay').fadeOut(100);
					$('#loading').css('top', '-30px');
				},
				headers: {
		            'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
		        }
			});
		},

		bindEvents : function () {
			window.onhashchange = this.router;
			$('#sessionModal').on('hidden.bs.modal', this.hiddenSession );
		},

		router : function () {
			var url = document.location.hash.replace('#', '');

			if (url != '') {
				self.changeColor(url);
			};

			self.isSession = 0;

            $('body').animate({scrollTop: 0},'slow');

			switch (url) {
				case '': {
					self.redirect('sessions');
				};break;
				case 'dashboard': {
					self.goToDashboard();
				};break;
				case 'courses': {
					self.goToCourses();
				};break;
				case 'sessions': {
					self.goToSessions();
					self.isSession = 1;
				};break;
				case 'contracts': {
					self.goToContracts();
				};break;
				case 'attendance': {
					self.goToAttendance();
				};break;
			}
		},

		redirect : function (url) {
			document.location.hash = url;
		},

		changeColor : function (id) {
			$('.menu-item').removeClass('active');
			$('#' + id).addClass('active');
		},

		validateEmail : function(type, value) {
			
			switch(type){
				case 'email': {
					re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
					result = re.test(value);
				};break;
				case 'phone': {
					re = /^[0-9]*$/i;
					result = re.test(value);
				};break;
				case 'required': {
					re = /\d/i;
					result = re.test(value);
				};break;
			}

			return result;
		},

		//============================================== Dashboard
		//
		goToDashboard : function () {
			$('#content').html('');
		},

		//============================================== Course
		//
		goToCourses : function () {

			$('#content').html( _.template($('#course-template').html()));
			this.getCourseList();
		},

		getCourseList : function () {
			$.ajax({
				url : '/api/course/',
				data : { pk : self.clubID }, 
				success : function(res) {
					courseListItems = _.template($('#course-item-template').html());

					_.each(res , function(eachModel){
						$('#content').find('#course-table tbody').append( courseListItems(eachModel) );
					});
					
					$('.course-list').click(self.coursereglist);
				}
			});
		},

		coursereglist : function () {
			var id = $(this).parent().parent().attr('id');
			self.courseID = id;
			$.ajax({
				url : '/api/enroll/course/club/0/',
				data : {
                    courseId : self.courseID
				},
				type : 'GET',
				cache : false,
				success : function(res) {
					$('#eachCourseRegList').html('<tr><th>حاضر</th><th>نام</th><th>نام خانوادگی</th><th>ایمیل</th><th>تلفن</th><th>حذف</th></tr><tr><td></td><td><input type="text" class="edit" id="firstname" name="firstname"></td><td><input type="text" class="edit" name="lastname" id="lastname"></td><td><input type="text" class="edit" name="email" id="email"></td><td><input type="text" class="edit" name="telephone" id="telephone"></td><td><button class="btn btn-sm btn-success courseRegListadd"><i class="fa fa-plus"></i></button></td></tr>');

					var template = _.template( $('#each-course-attendance-template').html() );

					res.forEach(function(item){
						_.extend(item, self.detectStatus(item.firstAccess), self.courseDeletePermission(item.user));
						$('#eachCourseRegList').append( template( item ) );
					});
					
					$('.courseRegListadd').click(self.addCourseItem);
					$('.courseRegListdelete').click(self.deleteCourseItem);
					$('.present-btn').click( self.approvePresent );
				}
			});

			$('#courseModal').modal('show');
		},

		addCourseItem : function () {
			var tr = $(this).parent().parent();
			
			var firstnameVal = tr.find('#firstname').val();
			var lastnameVal = tr.find('#lastname').val();
			var emailVal = tr.find('#email').val();
			var telephoneVal = tr.find('#telephone').val();
            var status = self.detectStatus(false);

			if(firstnameVal  != '' && lastnameVal  != ''){
				if (!self.validateEmail('email', emailVal) && emailVal != '') {
					alert('ایمیل شما صحیح نمی باشد!');
				};
				if (!self.validateEmail('phone', telephoneVal)) {
					alert('شماره شما صحیح نمی باشد!');
				};

				$.ajax({
					url : '/api/enroll/course/club/0/',
					type : 'POST',
					data : {
						courseId : self.courseID,
						firstName : firstnameVal,
						lastName : lastnameVal,
						eMail : emailVal,
						cellPhone : telephoneVal
					},
					cache : false,
					error : function (xhr, status, error) {
						if (xhr.status == 400) {
							alert('ظرفیت تکمیل است.');
						};
					},
					success : function(res) {

						$('<tr id="'+ res +'"><td>' + status.status + '</td><td colspan="2">'+ firstnameVal +' '+ lastnameVal +'</td><td>'+ emailVal +'</td><td>'+ telephoneVal +'</td><td><button class="btn btn-danger btn-sm sessionRegListdelete"><i class="fa fa-trash-o"></i></button></td></tr>').insertAfter('#eachCourseRegList tbody');
						tr.find('#firstname').val('');
						tr.find('#lastname').val('');
						tr.find('#email').val('');
						tr.find('#telephone').val('');

						$('.sessionRegListdelete').click(self.deleteItem);
					    $('.present-btn').click( self.approvePresent );
					}
				});
			}
		},

		deleteCourseItem : function () {
			var id = $(this).parent().parent().attr('id');
			res = confirm('آیا از حذف رکورد انتخاب شده مطمئن هستید ؟');
			if(res){
				var self = $(this);
				$.ajax({
					url : '/api/enroll/course/club/'+id+'/',
					type : 'DELETE',
					cache : false,
					success : function() {
						self.parent().parent().remove();
					}
				});
			}
		},

		//============================================== Sessions
		//
		goToSessions : function () {
			this.getSessions(0);
		},

		getSessions : function (weekId) {
			$.ajax({
				url : '/api/session/schedules/',
				type : 'GET',
				data : {
					club : self.clubID, week : weekId
				},
				cache : false,
				success : function(res) {
					self.sessionData = res;
					$('#content').html( _.template($('#sessions-template').html()));
					$('#next-week').click(self.generateNextWeek);
					$('#prev-week').click(self.generatePrevWeek);
					self.sessionAttendanceList();

					var sessionTemplate = $('#sessions-item-template').html();

					$('#sessions-holder').html('');
					var flag = 1;
					var startHours = 0;
					var endHours = 0;

		            res.forEach(function(session) {
		            	if(flag){
		            		flag = 0;
		            		self.generateTimeTable(session.begin, session.end, session.date, session.day);
		            		startHours = session.begin;
							endHours = session.end;	
							self.maxWeek = session.capacity;

							if (self.week == 0){
								$('#prev-week').hide();
							}else{
								$('#prev-week').show();
							}

							if (self.maxWeek - self.week == 1) {
								$('#next-week').hide();
							}else{
								$('#next-week').show();
							}
		            	}else{
		            		var right = (session.day + 1) * ($('#sessions-holder').innerWidth() / 8);
		            		var top = self.generateTop(session.begin, startHours) * 30;
		            		var height = (self.generateDuration(session.begin, session.end) / 2);
		            		var price = self.priceSeperator(session.price);

		            		var theme = sessionTemplate.replace(/<<id>>/g, session.cellid);
		            		theme = theme.replace(/<<top>>/g, top + 'px');
		            		theme = theme.replace(/<<right>>/g, right + 'px');
		            		theme = theme.replace(/<<height>>/g, height + 'px');
		            		theme = theme.replace(/<<price>>/g, price);
		            		theme = theme.replace(/<<begin>>/g, session.begin);
		            		theme = theme.replace(/<<end>>/g, session.end);
		            		theme = theme.replace(/<<capacity>>/g, session.capacity);
		            		
		            		if (session.status == 0) {
		            			theme = theme.replace(/<<backgroundColor>>/g, '#9E9E9E');
		            			theme = theme.replace(/<<noclick>>/g, ' action="noclick" ');
		            			theme = theme.replace(/<<title>>/g, '');
		            			theme = theme.replace(/<<popUpContent>>/g, 'data-content="در حال حاضر غیر فعال می باشد"');
		            		}else{
		            			if (session.capacity <= 0) {
		            				theme = theme.replace(/<<title>>/g, '');
		            				theme = theme.replace(/<<noclick>>/g, ' action="noclick" ');
		            				theme = theme.replace(/<<popUpContent>>/g, 'data-content="ظرفیت تکمیل است"');
		            			}else{
			            			theme = theme.replace(/<<title>>/g, 'title="برای انتخاب برنامه روی آن کلیک نمایید"');
			            			theme = theme.replace(/<<noclick>>/g, '');
			            			theme = theme.replace(/<<popUpContent>>/g, 'data-content="'+ session.begin +' - '+ session.end +' | ظرفیت : '+ session.capacity +' | قیمت : '+ price +' ریال"');
		            			}
		            		}

		            		if (session.capacity <= 0) {
		            			theme = theme.replace(/<<backgroundColor>>/g, '#FF8A80');
		            		};

		            		$('#sessions-holder').append(theme);

		            		$('[data-toggle="popover"]').popover();
		            	}
		            });
		            
		            $('.session').click(self.sessionItemClick);
		        }
			});
		},

		hiddenSession : function () {
			if (self.flagModifySessionList) {
				self.getSessions(self.week);
				self.sessionAttendanceList();
				self.flagModifySessionList = 0;
			};
		},

		//session-attendance-template
		sessionAttendanceList : function () {
			$.ajax({
				url : '/api/enroll/session/club/0/',
				data : {clubid : self.clubID}, 
				type : 'GET',
				cache : false,
				success : function(res) {
					$('#attendance-table').html('<tr><th>حاضر</th><th>نام و نام خانوادگی</th><th>تلفن</th><th>ساعت شروع</th><th>ساعت ‍پایان</th></tr>');
					var template =  _.template($('#session-attendance-template').html());

					res.forEach(function(item){

						_.extend(item, self.detectStatus(item.firstAccess));
						$('#attendance-table').append(template( item ));
					});

					$('.present-btn').click( self.approvePresent );
					
				}
			});
		},

		detectStatus : function (status) {
			if (!status) {
				res = {'status' : '<button class="btn btn-info present-btn"><i class="fa fa-check"></i></button>'};
				return res;
			};
			var res = {'status' : '<i class="fa fa-check"></i>'};
			return res;
		},

        sessionDeletePermission : function (userID) {
			if (self.clubOwnerID == userID) {
				res = {'deleteItem' : '<button class="btn btn-danger btn-sm sessionRegListdelete"><i class="fa fa-trash-o"></i></button>'};
				return res;
			};
			var res = {'deleteItem' : ''};
			return res;
		},

		courseDeletePermission : function (userID) {
			if (self.clubOwnerID == userID) {
				res = {'deleteItem' : '<button class="btn btn-danger btn-sm courseRegListdelete"><i class="fa fa-trash-o"></i></button>'};
				return res;
			};
			var res = {'deleteItem' : ''};
			return res;
		},

		approvePresent : function () {
			var item = $(this);
            var id = $(this).parent().parent().attr('id');
			$.ajax({
				url : '/api/access/',
				type : 'POST',
				data : {enrollid : id},
				cache : false,
				success : function() {
					item.replaceWith('<i class="fa fa-check success"></i>');
				}
			});
		},

		sessionItemClick : function () {
			var id = $(this).attr('id');

			$.ajax({
				url : '/api/enroll/session/',
				type : 'GET',
				cache : false,
				data : {
					club : self.clubID, week : self.week, cellid : id
				},
				success : function(res) {

					self.cellID = id;

					$('#eachSessionRegList').html('<tr><th>نام</th><th>نام خانوادگی</th><th>ایمیل</th><th>تلفن</th><th>حذف</th></tr><tr><td><input type="text" class="edit" id="firstname" name="firstname"></td><td><input type="text" class="edit" name="lastname" id="lastname"></td><td><input type="text" class="edit" name="email" id="email"></td><td><input type="text" class="edit" name="telephone" id="telephone"></td><td><button class="btn btn-sm btn-success sessionRegListadd"><i class="fa fa-plus"></i></button></td></tr>');


					var template = _.template($('#each-session-attendance-template').html());

					res.forEach(function(item){
                        _.extend(item, self.sessionDeletePermission(item.user));
						$('#eachSessionRegList').append( template( item ) );
					});
					
					$('.sessionRegListadd').click(self.addItem);
					$('.sessionRegListdelete').click(self.deleteItem);
				}
			});

			$('#sessionModal').modal('show');
		},

		addItem : function () {
			var tr = $(this).parent().parent();
			
			var firstnameVal = tr.find('#firstname').val();
			var lastnameVal = tr.find('#lastname').val();
			var emailVal = tr.find('#email').val();
			var telephoneVal = tr.find('#telephone').val();

			if(firstnameVal  != '' && lastnameVal  != ''){
				if (!self.validateEmail('email', emailVal) && emailVal != '') {
					alert('ایمیل شما صحیح نمی باشد!');
					return;
				};
				if (!self.validateEmail('phone', telephoneVal)) {
					alert('شماره شما صحیح نمی باشد!');
					return;
				};

				$.ajax({
					url : '/api/enroll/session/club/0/',
					type : 'POST',
					data : {
						club : self.clubID, week : self.week, cellid : self.cellID, firstName:firstnameVal, lastName:lastnameVal, eMail:emailVal, cellPhone:telephoneVal
					},
					cache : false,
					success : function(res) {

						self.flagModifySessionList = 1;
						$('<tr id="'+ res +'"><td colspan="2">'+ firstnameVal +' '+ lastnameVal +'</td><td>'+ emailVal +'</td><td>'+ telephoneVal +'</td><td><button class="btn btn-danger btn-sm sessionRegListdelete"><i class="fa fa-trash-o"></i></button></td></tr>').insertAfter('#eachSessionRegList tbody');
						tr.find('#firstname').val('');
						tr.find('#lastname').val('');
						tr.find('#email').val('');
						tr.find('#telephone').val('');

						$('.sessionRegListdelete').click(self.deleteItem);
					},
					error : function (xhr, status, error) {
						if (xhr.status == 400) {
							alert('ظرفیت تکمیل است.');
						};
					}
				});

				$('#sessionModal').modal('show');
			}
		},

		deleteItem: function () {
			var id = $(this).parent().parent().attr('id');
			res = confirm('آیا از حذف رکورد انتخاب شده مطمئن هستید ؟');
			if(res){
				var item = $(this);
				$.ajax({
					url : '/api/enroll/session/club/'+id+'/',
					type : 'DELETE',
					cache : false,
					success : function() {
                        self.flagModifySessionList = 1;
						item.parent().parent().remove();
					}
				});
			}
		},

		generateTimeTable : function (start, end, date, day) {

			slices = '<tr>';
			var days = ['ساعت','شنبه','یکشنبه','دوشنبه','سه شنبه','چهارشنبه','پنجشنبه','جمعه'];
			for (var i = 0; i < days.length; i++) {
				var curDate = new Date.parse(date).addDays(i - day - 1).toString("yyyy-MM-dd");
				var exactDate = toJalaali(parseInt(curDate.split('-')[0]), parseInt(curDate.split('-')[1]), parseInt(curDate.split('-')[2]));

				if(i > day){
					slices += '<td class="program2-title">' + days[i] + '<br>' + exactDate.jy + '/' + exactDate.jm + '/' + exactDate.jd + '</td>'; 
				}else{
					slices += '<td class="program2-title">' + days[i] + '</td>';
				}
			};
			slices += '</tr>';
			for (var i = parseInt(start.split(':')[0]); i < parseInt(end.split(':')[0]); i++) {
				var j = i + 1;
				slices += '<tr><td class="hours">'+ i + ' - ' + j +'</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>';
			};
			$('#content').find('#session-table').append(slices);
		},

		priceSeperator : function(price){
			var str = price.toString();
			res = '';
			var j = 0;
			for (var i = str.length - 1; i >= 0; i--) {
				if(j == 3){
					j = 0;
					res += ',';
				}
				j++;
				res += str[i];
			};
			var finalres = '';
			for (var i = res.length - 1; i >= 0; i--) {
				finalres += res[i];
			};
			return finalres;
		},

		generateTop : function(begin, startHours){
			var start = begin.split(':');
			var init = startHours.split(':');
			var hDiff = start[0] - init[0];
			var mDiff = start[1] - init[1];
			var top = hDiff + (mDiff / 60);
			return top;
		},

		generateDuration : function(begin, end){
			var start = begin.split(':');
			var finish = end.split(':');
			var hDiff = finish[0] - start[0];
			var mDiff = finish[1] - start[1];
			var duration = (hDiff * 60) + mDiff;
			return duration;
		},

		generateNextWeek : function () {
			$('#prev-week').show();
			if (self.week < self.maxWeek - 1) {
				self.week++;
				self.getSessions(self.week);
			};
		},

		generatePrevWeek : function () {
			$('#next-week').show();
			if(self.week > 0){
				self.week--;
				self.getSessions(self.week);
			}
		},

		toJalaliDate : function (date, keyword) {
			var keyword = keyword || 0;
			var date = date.split('T')[0].split('-');
			var finalDate = toJalaali(parseInt(date[0]), parseInt(date[1]), parseInt(date[2]));
			if (keyword != 0) {
				var res = {};
				res[keyword] = finalDate.jy + '/' + finalDate.jm + '/' + finalDate.jd;
				return res;
			};
			
			return finalDate.jy + '/' + finalDate.jm + '/' + finalDate.jd;
		},

		//============================================== Contracts
		//
		goToContracts : function () {
			$('#content').html( _.template($('#contracts-template').html()));
			this.getContractList();
		},

		getContractList : function () {
			$.ajax({
				url : '/api/agreement/list/',
				success : function(res) {
					courseListItems = _.template($('#contracts-item-template').html());

					_.each(res , function(eachModel){

						_.extend(eachModel, self.toJalaliDate(eachModel.created , 'beginTime'), self.toJalaliDate(eachModel.expiry_date , 'endTime'));
						$('#content').find('#contracts-table tbody').append( courseListItems(eachModel) );
					});
					
				}
			});
		},

		//============================================== Attendance
		//
		goToAttendance : function () {

		}

	}

})(jQuery)