(function () {
	//=========================================================

	var url = window.location.href.replace(BASEURL + '/', '').split('#')[0];

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

		                var thisTemplate1 = clubTemplate.replace(/<<link>>/g, BASEURL + '/directory/detail/' + club.pk + '/');
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
				j = i + 1;
				output += '<option value="'+ j +'">'+ Data.categories[i] +'</option>';
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
			this.cnf.region.change(this.districtChange);
			this.cnf.category.change(this.fieldChange);
			this.cnf.genre.change(this.categoryChange);
			this.cnf.title.on('keydown', this.titleChange);
			window.onhashchange = this.locator;
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

		locator : function () {
			var url = document.location.hash;
			var res = self.parseUrl(url);
			for (var key in res){
				$('#' + key).val(res[key]);
				if(key == 'price'){
					self.cnf.range.html(res[key]);
				}
			}
			self.getData(res);
		},

		getData : function (inputs) {

 			var allData = ['title', 'category', 'genre', 'gender', 'price_min', 'price_max', 'city', 'region']
			req = {};
			for (var i = 0; i < allData.length; i++) {
				var key = allData[i];
				if(typeof(inputs[key]) != 'undefined'){
					req[key] = inputs[key];
				}
			};
			
			$.ajax({
				url : BASEURL + '/api/directory/',
				data : req,
				success : function(res) {
					var clubTemplate = self.cnf.clubTemplate.html();

					self.cnf.content.html('');
		            res.results.forEach(function(club) {
		                var thisTemplate1 = clubTemplate.replace(/<<link>>/g, '#');
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
			var temp = url.split('#');
			if(temp == ''){
				return [];
			}

			var urlQuery = temp[1].split('/');

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
				j = i + 1;
				output += '<option value="'+ j +'">'+ Data.genre[i] +'</option>';
			}
			this.cnf.genre.append(output);

			var output = '';
			for(i=0;i < Data.categories.length;i++){
				j = i + 1;
				output += '<option value="'+ j +'">'+ Data.categories[i] +'</option>';
			}
			this.cnf.category.append(output);

			var output = '';
			for(i=0;i < Data.city.length;i++){
				j = i + 1;
				output += '<option value="'+ j +'">'+ Data.city[i] +'</option>';
			}
			this.cnf.city.append(output);
		}

	};

	//===============================================

	club = {
		
		init : function (cnf) {
			this.config = cnf;
			self = this;
			this.bindEventes();
			this.makeMapHeight();
			this.getSessions();
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

		getSessions : function (inputs) {
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