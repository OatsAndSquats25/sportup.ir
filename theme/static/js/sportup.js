(function () {
	home = {

		defaultImage : BASEURL + '/img/barbells.jpg',
		
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
		},

		getFeatureClubs : function () {
			$.ajax({
				url : BASEURL + '/api/directory/fav/',
				type : 'GET',
				
				success : function(res) {
					var clubTemplate = self.config.clubTemplate.html();

					self.config.contentHolder.html('');
		            res.forEach(function(club) {

		                var thisTemplate1 = clubTemplate.replace(/<<link>>/g, BASEURL + '/directory/detail/' + club.pk + '/');
		                if(club.imageCollection.length == 0){
		                	var thisTemplate2 = thisTemplate1.replace(/<<img>>/g, self.defaultImage);
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
				j = i + 1;
				output += '<option value="'+ j +'">'+ Data.categories[i] +'</option>';
			}
			this.config.categoriesFilter.append(output);
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
			self = this;
			this.generateFilters();
			this.cnf.content.css('height', this.cnf.window.innerHeight() - 231);
			this.locator();
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
			this.cnf.district.change(this.districtChange);
			this.cnf.field.change(this.fieldChange);
			this.cnf.category.change(this.categoryChange);
			this.cnf.clubname.on('keydown', this.clubNameChange);
			window.onhashchange = this.locator;
		},

		setUrl : function (urlQuery) {
			url = '';
			for (var i = 0; i < urlQuery.length; i++) {
				url += urlQuery[i];
				if(i != urlQuery.length - 1){
					url += '/';;
				}
			}
			document.location.hash = url;
		},

		genderChange : function () {
			hash = document.location.hash;
			var temp = hash.split('#');
			var urlQuery = temp[1].split('/');
			urlQuery[0] = ($(this).val() == 1) ? 'آقایان' : 'بانوان';
			self.setUrl(urlQuery); 
		},

		cityChange : function () {
			hash = document.location.hash;
			var temp = hash.split('#');
			var urlQuery = temp[1].split('/');
			urlQuery[1] = ($(this).val() == 0) ? 'شهر' : self.idToCity(parseInt($(this).val()));
			self.setUrl(urlQuery); 
		},

		districtChange : function () {
			hash = document.location.hash;
			var temp = hash.split('#');
			var urlQuery = temp[1].split('/');
			urlQuery[2] = ($(this).val() == 0) ? 'منطقه' : $(this).val();
			self.setUrl(urlQuery); 
		},

		fieldChange : function () {
			hash = document.location.hash;
			var temp = hash.split('#');
			var urlQuery = temp[1].split('/');
			urlQuery[3] = ($(this).val() == 0) ? 'فیلد' : $(this).val();
			self.setUrl(urlQuery);
		},

		categoryChange : function () {
			hash = document.location.hash;
			var temp = hash.split('#');
			var urlQuery = temp[1].split('/');
			urlQuery[4] = ($(this).val() == 0) ? 'گروه' : $(this).val();
			self.setUrl(urlQuery);
		},

		clubNameChange : function (e) {
			if (e.which === self.ENTER_KEY) {
				hash = document.location.hash.split('#');
				var urlQuery = hash[1].split('/');
				urlQuery[6] = ($(this).val() == '') ? 'نام' : $(this).val();
				self.setUrl(urlQuery);
			}
		},

		locator : function () {
			var url = document.location.hash;
			var res = (url == "") ? self.startUrl() : self.parseUrl(url);
			if(res != "start"){
				self.getData(res);
			}
		},

		startUrl : function () {
			document.location.hash = 'آقایان/تهران/منطقه/فیلد/گروه/10000/نام';
			return "start";
		},

		getData : function (inputs) {
			$.ajax({
				url : 'http://localhost:8000/data',
				type : 'GET',
				data : {
					gender : inputs[0],
					city : inputs[1],
					district : inputs[2],
					field : inputs[3],
					category : inputs[4],
					price : inputs[5],
					clubname : inputs[6]
				},
				success : function(res) {
					var clubTemplate = self.cnf.clubTemplate.html();

					self.cnf.content.html('');
		            res.results.forEach(function(club) {
		                var thisTemplate1 = clubTemplate.replace(/<<link>>/g, '#');
		                var thisTemplate2 = thisTemplate1.replace(/<<img>>/g, club.image);
		                var thisTemplate3 = thisTemplate2.replace(/<<logo>>/g, club.logo);
		                var thisTemplate4 = thisTemplate3.replace(/<<title>>/g, club.title);

		                self.cnf.content.append(thisTemplate4);
		            });
				}
			});
		},

		parseUrl : function (url) {
			var temp = url.split('#');
			var urlQuery = temp[1].split('/');
			var gender = (urlQuery[0] == "آقایان") ? 1 : 2;
			var city = this.cityDetector(urlQuery[1]);
			var district = (urlQuery[2] == "منطقه") ? 0 : parseInt(urlQuery[2]);
			var field = (urlQuery[3] == "فیلد") ? 0 : parseInt(urlQuery[3]);
			var category = (urlQuery[4] == "گروه") ? 0 : parseInt(urlQuery[4]);
			var price = (urlQuery[5] == "قیمت") ? 0 : parseInt(urlQuery[5]);
			var name = (urlQuery[6] == "نام") ? 0 : urlQuery[6];
			var res = [gender, city, district, field, category, price, name];
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
			this.cnf.disctrictFilter.append(output);

			var output = '';
			for(i=0;i < Data.categories.length;i++){
				j = i + 1;
				output += '<option value="'+ j +'">'+ Data.categories[i] +'</option>';
			}
			this.cnf.categoriesFilter.append(output);
		},

		changeRange : function () {
			self.cnf.range.html($(this).val());
			hash = document.location.hash.split('#');
			var urlQuery = hash[1].split('/');
			urlQuery[5] = $(this).val();
			self.setUrl(urlQuery);
		}

	};

	//===============================================

	club = {
		
		init : function (cnf) {
			this.config = cnf;
			self = this;
			this.bindEventes();
			this.makeMapHeight();
			//this.generateTimeTable();
			this.getData();
		},

		makeMapHeight : function () {
			var height = this.config.program1.offset().top - 50;
			var mapTop = this.config.map.offset().top;
			this.config.map.css('height', height - mapTop);
		},

		bindEventes : function () {
			this.config.window.scroll(this.scrollToBottom);
			this.config.goToCourse.click(this.goToCourseAction);
			this.config.goToSession.click(this.goToSessionAction);
			this.config.goToTop.click(this.goToTopAction);
		},

		scrollToBottom : function () {
			var varscroll = $(this).scrollTop();
			var max = self.config.program1.offset().top;

			/*if(varscroll == 0){
				$('#club-subnav').hide();
				$('#box-club-info').hide();
				$('#box').removeAttr('style');
				return;
			}

			if(varscroll <= max - 200){
				$('#club-subnav').show();
				$('#box-club-info').slideDown(1000);
				$('#box').css({
					'position' : 'fixed',
					'top' : '101px'
				});
			}
		
			if(varscroll >= 360){
				$('#club-subnav').show();
				$('#box-club-info').slideDown(1000);
				$('#box').css({
					'position' : 'fixed',
					'top' : '101px'
				});
				$('#go-to-top').fadeIn();
			}else{
				$('#club-subnav').hide();
				$('#box-club-info').hide();
				$('#box').removeAttr('style');
				$('#go-to-top').hide();
			}*/
		},

		getData : function (inputs) {
			$.ajax({
				url : 'http://localhost:8000/datajson',
				type : 'GET',
				data : {
					id : 1
				},
				success : function(res) {
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
		            	}else{
		            		var right = (session.day + 1) * 125;
		            		var top = self.generateTop(session.begin, startHours) * 30;
		            		var height = (self.generateDuration(session.begin, session.end) / 2);
		            		var price = self.priceSeperator(session.price);
		            		var thisTemplate1 = sessionTemplate.replace(/<<id>>/g, session.prgid);
		            		var thisTemplate2 = thisTemplate1.replace(/<<top>>/g, top + 'px');
		            		var thisTemplate3 = thisTemplate2.replace(/<<right>>/g, right + 'px');
		            		var thisTemplate4 = thisTemplate3.replace(/<<height>>/g, height + 'px');
		            		var thisTemplate5 = thisTemplate4.replace(/<<price>>/g, price);
		            		var thisTemplate6 = thisTemplate5.replace(/<<begin>>/g, session.begin);
		            		var thisTemplate7 = thisTemplate6.replace(/<<end>>/g, session.end);
		            		var thisTemplate8 = thisTemplate7.replace(/<<capacity>>/g, session.capacity);
		            		
		            		self.config.sessionsHolder.append(thisTemplate8);
		            	}
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
			var exactDate = toJalaali(parseInt(date.split('-')[0]), parseInt(date.split('-')[1]), parseInt(date.split('-')[2]));
			
			slices = '<tr>';
			var days = ['ساعت','شنبه','یکشنبه','دوشنبه','سه شنبه','چهارشنبه','پنجشنبه','جمعه'];
			for (var i = 0; i < days.length; i++) {
				if(i > day){
					slices += '<td>' + days[i] + '<br>' + exactDate.jy + '/' + exactDate.jm + '/' + (exactDate.jd + (i - day - 1))  + '</td>'; 
				}else{
					slices += '<td>' + days[i] + '</td>';
				}
			};
			slices += '</tr>';
			for (var i = parseInt(start.split(':')[0]); i <= parseInt(end.split(':')[0]); i++) {
				var j = i + 1;
				slices += '<tr><td class="hours">'+ i + ' - ' + j +'</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>/tr>';
			};
			this.config.program2.find('table').append(slices);
		},

		goToCourseAction : function () {
			var program1Top = self.config.program1.offset().top;
			self.config.body.animate({scrollTop: program1Top - 80},'slow');
		},

		goToSessionAction : function () {
			var program2Top = self.config.program2.offset().top;
			self.config.body.animate({scrollTop: program2Top - 80},'slow');
		},

		goToTopAction : function () {
			self.config.body.animate({scrollTop: 0},'slow');
		}
	}	


})(jQuery);