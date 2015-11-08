(function () {
	//=========================================================

	var url = window.location.href.replace(BASEURL + '/', '').split('#')[0];

	if (parseInt($('nav').css('top')) == -100) {
		$('.alert').css('top', 0);
	};

	if(url != 'search'){
		$('#title').on('keydown', function(e){
			if (e.which === 13) {
				var titleContent = $(this).val();
				if(titleContent != ''){
					window.location = BASEURL + '/search#title=' + titleContent;
				}
			}
		});

		$('#titleBtn').click(function(){
			var titleContent = $('#titleHome').val();
			if(titleContent != ''){
				window.location = BASEURL + '/search#title=' + titleContent;
			}
		});
	}

	defaultImage = BASEURL + '/static/img/barbells.jpg';

	//===========================================================
	
	home = {

		init : function (cnf) {
			this.config = cnf;
			self = this;
			this.bindEventes();
			this.scrollMenu();
			this.generateCategory();
			this.getFeatureClubs();
			this.config.aboutBox.css('height', this.config.window.innerHeight());

			$.ajaxSetup({
				cache : true,
				beforeSend : function() {
					$('.loading').fadeIn(100);
				},
				complete : function() {
					$('.loading').fadeOut(100);
				}
			});
		},

		bindEventes : function () {
			this.config.window.scroll(this.scrollMenu);
			this.config.aboutTop.click(this.generateAboutTop);
			this.config.goToTop.click(this.goToTopAction);
			this.config.category.change(this.changeCategory);
			this.config.newsletterBtn.click(this.newsLetterSubscriber);
		},

		validateEmail : function(email) {
		    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
		    return re.test(email);
		},

		newsLetterSubscriber : function () {
			var email = self.config.newsletter.val();
			if(self.validateEmail(email) == false){
				alert('ایمیل شما اشتباه وارد شده است لطفا مجدد وارد نمایید.');
				return;
			}

			$.ajax({
				url : 'https://app.mailerlite.com/api/v1/subscribers/2081231/',
				type : 'POST',
				data : {
					apiKey : '6155b1d49ae1f44661d78c6a2de46adc',
					id : 2081231,
					email : email
				},
				success : function(res) {
					self.config.newsLetterHolder.html('ضمن تشکر از عضویت شما یک ایمیل جهت تایید برای شما ارسال گردید.')
				}

			});
		},

		changeCategory : function () {
			var category = $(this).val();
			if(category != 0){
				window.location = BASEURL + '/search#category=' + category;
			}
		},

		getFeatureClubs : function () {
			$.ajax({
				url : BASEURL + '/api/directory/fav/',
				type : 'GET',
				
				success : function(res) {
					var clubTemplate = self.config.clubTemplate.html();

					self.config.contentHolder.html('');
		            res.forEach(function(club) {

		                var thisTemplate1 = clubTemplate.replace(/<<link>>/g, BASEURL + '/club#' + club.id);
		                if(club.imageCollection.length == 0){
		                	var thisTemplate2 = thisTemplate1.replace(/<<img>>/g, defaultImage);
		                }else{
		                	var thisTemplate2 = thisTemplate1.replace(/<<img>>/g, club.imageCollection[0].imageFile);
		                }
		                var thisTemplate3 = thisTemplate2.replace(/<<logo>>/g, club.logo);
		                var thisTemplate4 = thisTemplate3.replace(/<<title>>/g, club.title);

		                self.config.contentHolder.append(thisTemplate4);
		            });
				}
			});
		},

		generateAboutTop : function () {
			self.config.aboutBox.slideDown();
		},

		generateCategory : function () {
			var output = '';
			for(i=0;i < Data.categories.length;i++){
				output += '<option value="'+ Data.categories[i].id +'">'+ Data.categories[i].title +'</option>';
			}
			this.config.category.append(output);
		},

		scrollMenu : function () {
			var varscroll = $(this).scrollTop();

			if($("#about-user:visible").length == 1){
				if(varscroll >= self.config.window.innerHeight()){
					self.config.aboutBox.hide();
					self.config.body.scrollTop(0);
				}
				return;
			}

			if(varscroll >= 600){
				$('.nav').hide();
				$('nav').css('top', 0);
				$('#go-to-top').fadeIn();
			}else{
				$('.nav').show();
				$('nav').removeAttr('style');
				$('#go-to-top').hide();
			}
		},

		goToTopAction : function () {
			self.config.body.animate({scrollTop: 0},'slow');
		}
	}	

	//===============================================
	//
	search = {

		ENTER_KEY : 13,

		ESC_KEY : 27,

		init : function (config) {
			this.cnf = config;
			//hiding boxes==========
			this.cnf.gender.hide();
			this.cnf.priceBar.hide();
			this.cnf.filters.css('height', 160);
			this.cnf.selectHolder.find('select').css('width', 'calc(25% - 4px)');
			//======================
			this.cnf.content.css('height', this.cnf.window.innerHeight() - 155);
			//this.cnf.content.css('height', this.cnf.window.innerHeight() - 231);
			self = this;
			this.generateFilters();
			this.locator(1);
			this.bindEventes();

			$.ajaxSetup({
				cache : true,
				beforeSend : function() {
					$('.loading').fadeIn(100);
				},
				complete : function() {
					$('.loading').fadeOut(100);
				}
			});

		},

		bindEventes : function () {
			this.cnf.rangeBar.change(this.changeRange);
			this.cnf.gender.change(this.genderChange);
			this.cnf.city.change(this.cityChange);
			this.cnf.region.change(this.districtChange);
			this.cnf.category.change(this.fieldChange);
			this.cnf.genre.change(this.categoryChange);
			this.cnf.title.on('keydown', this.titleChange);
			self.cnf.window.resize(this.searchItemsHeightFix);
			window.onhashchange = this.locator;
			// Infinite scroll
			//$('#content').scroll(this.infinitescroll);
		},

		infinitescroll : function () {
			var item = $(this).context;
			if (item.offsetHeight + item.scrollTop == item.scrollHeight) {
				if (self.nextPageURL && self.flagOnceInfiniteRequest) {
					self.flagOnceInfiniteRequest = 0;
					//self.getData(self.Query, self.nextPageURL, true);
				};
			};
		},

		searchItemsHeightFix : function () {
			self.cnf.content.css('height', self.cnf.window.innerHeight() - 155);
		},

		setUrl : function (urlQuery) {
			url = '';
			var i = 0;
			var max = self.size(urlQuery) - 1;
			for (var key in urlQuery){
				url = url + key + '=' + urlQuery[key];
				if(i != max){
					url += '/';
				}
				i++;
			}
			
			document.location.hash = url;
		},

		size : function(obj) {
		    var size = 0, key;
		    for (key in obj) {
		        if (obj.hasOwnProperty(key)) size++;
		    }
		    return size;
		},

		genderChange : function () {
			var urlQuery = self.parseUrl(document.location.hash);

			if($(this).val() == 0){
				if(typeof(urlQuery['gender']) != "undefined"){
					delete urlQuery["gender"];
				}
			}else{
				urlQuery['gender'] = $(this).val();
			}	
			
			self.setUrl(urlQuery); 
		},

		cityChange : function () {
			var urlQuery = self.parseUrl(document.location.hash);

			if($(this).val() == 0){
				if(typeof(urlQuery['city']) != "undefined"){
					delete urlQuery["city"];
				}
			}else{
				urlQuery['city'] = $(this).val();
			}	
			
			self.setUrl(urlQuery);
		},

		districtChange : function () {
			var urlQuery = self.parseUrl(document.location.hash);

			if($(this).val() == 0){
				if(typeof(urlQuery['region']) != "undefined"){
					delete urlQuery["region"];
				}
			}else{
				urlQuery['region'] = $(this).val();
			}	
			
			self.setUrl(urlQuery);
		},

		fieldChange : function () {
			var urlQuery = self.parseUrl(document.location.hash);

			if($(this).val() == 0){
				if(typeof(urlQuery['category']) != "undefined"){
					delete urlQuery["category"];
				}
			}else{
				urlQuery['category'] = $(this).val();
			}	

			self.setUrl(urlQuery);
		},

		categoryChange : function () {
			var urlQuery = self.parseUrl(document.location.hash);

			if($(this).val() == 0){
				if(typeof(urlQuery['genre']) != "undefined"){
					delete urlQuery["genre"];
				}
			}else{
				urlQuery['genre'] = $(this).val();
			}	
			
			self.setUrl(urlQuery);
		},

		changeRange : function (e) {
			self.cnf.range.html($(this).val());
			var urlQuery = self.parseUrl(document.location.hash);

			if($(this).val() == ''){
				if(typeof(urlQuery['price']) != "undefined"){
					delete urlQuery["price"];
				}
			}else{
				urlQuery['price'] = $(this).val();
			}	
			self.setUrl(urlQuery);
		},

		titleChange : function (e) {
			var urlQuery = self.parseUrl(document.location.hash);
			if (e.which === self.ENTER_KEY) {
				if($(this).val() == ''){
					if(typeof(urlQuery['title']) != "undefined"){
						delete urlQuery["title"];
					}
				}else{
					urlQuery['title'] = $(this).val();
				}	
				
				self.setUrl(urlQuery);
			}
		},

		locator : function (first) {
			var detector = (first == 1)? 1 : 0;
			var url = document.location.hash;

			if (detector && url.replace('#', '') == '') {
				return self.startURL();
			}

			return self.callData(url);
		},

		callData : function (url) {
			self.cookieSeter('search', url);

			var res = self.parseUrl(url);
			for (var key in res){
				$('#' + key).val(res[key]);
				if(key == 'price'){
					self.cnf.range.html(res[key]);
				}
			}
			self.getData(res);
		},

		startURL : function(){
			var url = this.cookieGeter('search');

			if(url){
				return self.redirect(url);
			}

			return self.redirect('title=');
		},

		redirect : function (url) {
			document.location.hash = url;
		},

		cookieGeter : function(cookieName){
			
			var cookies = document.cookie.split(';');
				
			for (var i = 0; i < cookies.length; i++) {

				if (cookies[i].search('search=') != -1) {
					var temp = cookies[i].trim().replace('search=', '');
					return decodeURI(temp);
				}
			}

			return false;
		},

		cookieSeter : function(cookieName, url){
			document.cookie = cookieName + "=" + encodeURI(url);
		},

		getData : function (inputs) {

 			var allData = ['title', 'category', 'genre', 'gender', 'price_min', 'price_max', 'city', 'region'];
			req = {};
			for (var i = 0; i < allData.length; i++) {
				var key = allData[i];
				if(typeof(inputs[key]) != 'undefined'){
					req[key] = inputs[key];
				}
			};
			
			$.ajax({
				url : '/api/directory/',
				data : req,
				success : function(res) {
					if (res.count == 0) {
						return self.cnf.content.html('<div class="noresult">نتیجه ای یافت نشد.</div>');
					}
					self.flagOnceInfiniteRequest = 1;
					var clubTemplate = self.cnf.clubTemplate.html();

					self.cnf.content.html('');
		            res.results.forEach(function(club) {
                        if (club.hasAgreement == 0)
                            var thisTemplate0 = clubTemplate.replace(/<<hasAgreement>>/g, 'hidden');
                        else
                            var thisTemplate0 = clubTemplate.replace(/<<hasAgreement>>/g, '');
		                var thisTemplate1 = thisTemplate0.replace(/<<link>>/g, '/club#' + club.id);
						if(club.imageCollection.length == 0){
		                	var thisTemplate2 = thisTemplate1.replace(/<<img>>/g, defaultImage);
		                }else{
		                	var thisTemplate2 = thisTemplate1.replace(/<<img>>/g, club.imageCollection[0].imageFile);
		                }
		                var thisTemplate3 = thisTemplate2.replace(/<<logo>>/g, club.logo);
		                var thisTemplate4 = thisTemplate3.replace(/<<title>>/g, club.title);

		                self.cnf.content.append(thisTemplate4);
		            });
				}
			});
		},

		parseUrl : function (url) {
			var temp = url.replace('#', '');
			if(temp == ''){
				return [];
			}

			var urlQuery = temp.split('/');

			var res = [];
			for (var i = 0; i < urlQuery.length; i++) {
				var key = urlQuery[i].split('=')[0];
				var value = urlQuery[i].split('=')[1];
				res[key] = value;
			};

			return res;
		},

		cityDetector : function (cityname) {
			switch(cityname){
				case "تهران" : {return 1}
				case "قم" : {return 2}
			}
		},

		idToCity : function (cityid) {
			switch(cityid){
				case 1 : {return 'تهران'}
				case 2 : {return 'قم'}
			}
		},

		generateFilters : function () {
			var output = '';
			for(i=1;i<=22;i++){
				output += '<option value="'+ i +'">منطقه '+ i +'</option>';
			}
			this.cnf.region.append(output);

			var output = '';
			for(i=0;i < Data.genre.length;i++){
				output += '<option value="'+ Data.genre[i].id +'">'+ Data.genre[i].title +'</option>';
			}
			this.cnf.genre.append(output);

			var output = '';
			for(i=0;i < Data.categories.length;i++){
				output += '<option value="'+ Data.categories[i].id +'">'+ Data.categories[i].title +'</option>';
			}
			this.cnf.category.append(output);

			var output = '';
			for(i=0;i < Data.city.length;i++){
				output += '<option value="'+ Data.city[i].id +'">'+ Data.city[i].title +'</option>';
			}
			this.cnf.city.append(output);
		}

	};

	//===============================================

	club = {

		defaultURL : 1,

		init : function (cnf) {
			this.config = cnf;
			self = this;
			this.week = 0;
			this.club = parseInt(document.location.hash.replace('#', ''));
			this.bindEventes();
			this.makeMapHeight();
			this.locator();
		},

		bindEventes : function () {
			this.config.goToCourse.click(this.goToCourseAction);
			this.config.goToSession.click(this.goToSessionAction);
			this.config.goToTop.click(this.goToTopAction);
			this.config.nextWeek.click(this.generateNextWeek);
			this.config.prevWeek.click(this.generatePrevWeek);
			window.onhashchange = this.locator;
		},

		locator : function () {
			var url = document.location.hash;

			if (url.replace('#', '') == '') {
				return self.startURL();
			}else{
				self.cookieSeter('club', url);
			}

			self.club = parseInt(url.replace('#', ''));

			self.getData(self.club);
			self.getCourse(self.club);
			self.getSessions(self.club, this.week);
		},

		startURL : function(){
			var url = this.cookieGeter('club');

			if(url){
				return self.redirect(url);
			}

			return self.redirect(self.defaultURL);
		},

		redirect : function (url) {
			document.location.hash = url;
		},

		cookieGeter : function(cookieName){
			
			var cookies = document.cookie.split(';');

				
			for (var i = 0; i < cookies.length; i++) {
				if (cookies[i].search('club=') == 1) {
                    console.log(cookies[i].trim().replace('club=', ''));
					return cookies[i].trim().replace('club=', '');
				}
			}

			return false;
		},

		cookieSeter : function(cookieName, url){
			document.cookie = cookieName + "=" + url;
		},

		generateNextWeek : function () {
			if (self.week < self.maxWeek - 1) {
				self.week++;
				self.getSessions(self.club, self.week);
			};
		},

		generatePrevWeek : function () {
			if(self.week > 0){
				self.week--;
				self.getSessions(self.club, self.week);
			}
		},

		makeMapHeight : function () {
			var height = this.config.sports.offset().top + this.config.sports.innerHeight();
			var mapTop = this.config.map.offset().top;
			this.config.map.css('height', height - mapTop);
		},

		setTitle : function (title) {
			document.title = title;
		},

		getData : function (clubId) {
			$.ajax({
				url : BASEURL + '/api/directory/' + clubId + '/',
				type : 'GET',
				//data : {
				//	pk : clubId
				//},
				cache : false,
				success : function(res) {
					self.clubId = res.id;
					self.setTitle(res.complexName);

					$('.logo-image').attr('src', res.logo);
					$('#club-title').html(res.complexName);
					$('#club-address').html(res.locationAddress[0].address);
					$('#club-phone').html(res.phone + ' | ' + res.cell);
					$('#description').html(res.complexSummary);
					$('#summary').html(res.summary);
					$('#club-web').html('<a href="'+ res.website +'" target="_blank">'+ res.website +'</a>');
					
					$('#subclub-titles').html('');
					$('.category-title').html(res.title);

					if(res.clubs.length){
						res.clubs.forEach(function(club){
							$('#subclub-titles').append('<li role="presentation"><a class="club-item" id="' + club.id + '" role="tab" data-toggle="tab">' + club.title + '</a></li>');
						});
					}

					$('.club-item[id='+ res.id +']').parent().addClass('active');

					if(res.imageCollection.length){
						$('#image-holder').html('');
						res.imageCollection.forEach(function(image){
							$('#image-holder').append('<div class="item"><img src="' + image.imageFile + '" width="100%"></div>');
						});
						$('#image-holder').find('div.item:first').addClass('active');
					}
					
					self.makeMapHeight();

					//OTHER TABS EVENT
					$('.club-item').click(function(){
						document.location.hash = $(this).attr('id');
					});

					var coordinate = res.locationAddress[0].coordinate.match(/\(.+\)/g)[0].replace('(', '').replace(')', '').split(' ');
					self.googleMap(coordinate[0], coordinate[1]);
				}
			});
		},

		googleMap : function (lat, lang) {
			google.maps.event.addDomListener(window, 'load', initialize(lang, lat));
		},

		getCourse : function (clubId) {
			$.ajax({
				url : BASEURL + '/api/course/',
				type : 'GET',
				data : {
					pk : clubId
				},
				cache : false,
				error : function (xhr,status,error) {
					self.config.program1.hide();
				},
				success : function(res, string, xhr) {
					if(xhr.status == 204){
						return self.config.program1.hide();
					}
					self.config.program1.show();
					self.courseData = res;

					var sessionTemplate = self.config.courseTemplate.html();

					self.config.courseHolder.html('<tr style="background-color:#888;color:#fff;"><td class="program1-title">برنامه ها</td><td class="program1-title">ظرفیت</td><td class="program1-title">هزینه(ریال)</td><td class="program1-title">جنسیت</td><td class="program1-title">تاریخ شروع</td><td class="program1-title">تاریخ پایان</td><td class="program1-title">مهلت ثبت نام</td><td class="program1-title">ثبت نام</td></tr>');
							            
		            res.forEach(function(course) {

	            		temp = sessionTemplate.replace(/<<title>>/g, course.title);
	            		temp = temp.replace(/<<capacity>>/g, course.remainCapacity);
	            		temp = temp.replace(/<<price>>/g, self.priceSeperator(course.price));
	            		temp = temp.replace(/<<gender>>/g, course.genderLimit);

	            		if (course.usageBeginDate == null) {
	            			temp = temp.replace(/<<begin>>/g, '-');
	            		}else{
	            			temp = temp.replace(/<<begin>>/g, self.readyDate(course.usageBeginDate));
	            		}

	            		if (course.usageEndDate == null) {
	            			temp = temp.replace(/<<end>>/g, '-');
	            		}else{
	            			temp = temp.replace(/<<end>>/g, self.readyDate(course.usageEndDate));
	            		}
	            		
	            		if (course.expiry_date == null) {
	            			temp = temp.replace(/<<deadline>>/g, '-');
	            		}else{
	            			temp = temp.replace(/<<deadline>>/g, self.readyDateTime(course.expiry_date));
	            		}

	            		temp = temp.replace(/<<id>>/g, course.id);
	            		
	            		self.config.courseHolder.append(temp);
		            });

					$('.course-item').click(function(){
						var id = $(this).attr('id');
						self.courseData.forEach(function(course){
							if (course.id == id) {
								var sessionTemplate = self.config.courseModalTemplate.html();
								
								var temp = sessionTemplate.replace(/<<title>>/g, course.title);
								if (course.ageMin == 0) {
									temp = temp.replace(/<<age>>/g, 'محدودیت سنی ندارد');
								}else {
									temp = temp.replace(/<<age>>/g, course.ageMin + ' تا ' + course.ageMax + ' سال');
								}
								
								temp = temp.replace(/<<gender>>/g, course.genderLimit);

								if (course.ensurance) {
										temp = temp.replace(/<<ensurance>>/g, 'دارد');
									}else{
										temp = temp.replace(/<<ensurance>>/g, 'ندارد');				
									}

								if (course.usageBeginDate == null) {
			            			temp = temp.replace(/<<begin>>/g, '-');
			            		}else{
			            			temp = temp.replace(/<<begin>>/g, self.readyDate(course.usageBeginDate));
			            		}

			            		if (course.usageEndDate == null) {
			            			temp = temp.replace(/<<end>>/g, '-');
			            		}else{
			            			temp = temp.replace(/<<end>>/g, self.readyDate(course.usageEndDate));
			            		}
								temp = temp.replace(/<<price>>/g, self.priceSeperator(course.price) + 'ریال');
								
								if (course.description == '') {
									temp = temp.replace(/<<description>>/g, '');
								}else {
									temp = temp.replace(/<<description>>/g, '<tr><td colspan="7">توضیحات'+ course.description +'</td></tr>');
								}

								temp = temp.replace(/<<clubid>>/g, self.clubId);
								temp = temp.replace(/<<courseid>>/g, course.id);

								self.config.courseApproveHolder.html(temp);
							}
						});

						self.config.courseModal.modal('show');
					});
				}
			});
		},

		readyDate : function (date) {
			var finalDate = toJalaali(parseInt(date.split('-')[0]), parseInt(date.split('-')[1]), parseInt(date.split('-')[2]));
			return finalDate.jy + '/' + finalDate.jm + '/' + finalDate.jd;
		},

		readyDateTime : function (dateTime) {
			var date = dateTime.split('T')[0];
			var finalDate = toJalaali(parseInt(date.split('-')[0]), parseInt(date.split('-')[1]), parseInt(date.split('-')[2]));
			return finalDate.jy + '/' + finalDate.jm + '/' + finalDate.jd;
		},

		getSessions : function (clubId, weekId) {
			self.config.loadingSession.show();
			$.ajax({
				url : BASEURL + '/api/session/schedules/',
				type : 'GET',
				data : {
					club : clubId,
					week : weekId
				},
				cache : false,
				error : function (xhr,status,error){
					self.config.program2.hide();
				},
				success : function(res, string, xhr) {
					if(xhr.status == 204){
						return self.config.program2.hide();
					}
					self.config.program2.show();
					self.sessionData = res;

					self.config.loadingSession.hide();
					var sessionTemplate = self.config.sessionTemplate.html();

					self.config.sessionsHolder.html('');
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
		            		var right = (session.day + 1) * (self.config.sessions.innerWidth() / 8);
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

		            		self.config.sessionsHolder.append(theme);
		            	}

		            	$('.session').click(function(){
							var id = $(this).attr('id');
							self.sessionData.forEach(function(session){

								if (session.cellid == parseInt(id)) {
									var sessionTemplate = self.config.sessionModalTemplate.html();
									
									var temp = sessionTemplate.replace(/<<title>>/g, session.title);
									if (session.ageMin == 0) {
										temp = temp.replace(/<<age>>/g, 'محدودیت سنی ندارد');
									}else {
										temp = temp.replace(/<<age>>/g, session.ageMin + ' تا ' + session.ageMax + ' سال');
									}
									
									temp = temp.replace(/<<gender>>/g, session.genderLimit);

									if (session.ensurance) {
										temp = temp.replace(/<<ensurance>>/g, 'دارد');
									}else{
										temp = temp.replace(/<<ensurance>>/g, 'ندارد');				
									}

				            		temp = temp.replace(/<<begin>>/g, session.begin);
				            		temp = temp.replace(/<<end>>/g, session.end);
									temp = temp.replace(/<<price>>/g, self.priceSeperator(session.price) + 'ریال');
									
									if (session.description == '') {
										temp = temp.replace(/<<description>>/g, '');
									}else {
										temp = temp.replace(/<<description>>/g, '<tr><td colspan="7">توضیحات'+ session.description +'</td></tr>');
									}

									temp = temp.replace(/<<clubid>>/g, self.clubId);
									temp = temp.replace(/<<week>>/g, self.week);
									temp = temp.replace(/<<cellid>>/g, session.cellid);

									self.config.sessionApproveHolder.html(temp);
								}
							});

							if ($(this).attr('action') != 'noclick') {
								self.config.sessionModal.modal('show');
							};
						});

		            	$('[data-toggle="popover"]').popover();
		            });
				}
			});
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

		generateTimeTable : function (start, end, date, day) {

			this.config.program2.find('table').html('');
			slices = '<tr>';
			var days = ['ساعت','شنبه','یکشنبه','دوشنبه','سه شنبه','چهارشنبه','پنجشنبه','جمعه'];
			for (var i = 0; i < days.length; i++) {
				var curDate = new Date.parse(date).addDays(i - day - 1).toString("yyyy-MM-dd");
				var exactDate = toJalaali(parseInt(curDate.split('-')[0]), parseInt(curDate.split('-')[1]), parseInt(curDate.split('-')[2]));

				if(i > 0){
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
			this.config.program2.find('table').append(slices);
		},

		goToCourseAction : function () {
			var program1Top = self.config.program1.offset().top;
			self.config.body.animate({scrollTop: program1Top - 100},'slow');
		},

		goToSessionAction : function () {
			var program2Top = self.config.program2.offset().top;
			self.config.body.animate({scrollTop: program2Top - 100},'slow');
		},

		goToTopAction : function () {
			self.config.body.animate({scrollTop: 0},'slow');
		}
	}	


})(jQuery);