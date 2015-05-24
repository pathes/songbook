(function() {
    'use strict';

    angular.module('sbUtils', [])

        .constant('sbUrl', [
            {
                caption: 'menuHome',
                url: '/',
                templateUrl: '/static/songbook/html/home.html',
                controller: 'sbHomeController',
                inMenu: true
            },
            {
                caption: 'menuSongs',
                url: '/song',
                templateUrl: '/static/songbook/html/songs.html',
                controller: 'sbSongsController',
                inMenu: true
            },
            {
                caption: 'menuSong',
                url: '/song/:songId',
                templateUrl: '/static/songbook/html/song.html',
                controller: 'sbSongController',
                inMenu: false
            },
            {
                caption: 'menuSonglists',
                url: '/songlist',
                templateUrl: '/static/songbook/html/songlists.html',
                controller: 'sbSonglistsController',
                inMenu: true
            },
            {
                caption: 'menuSonglist',
                url: '/songlist/:songlistId',
                templateUrl: '/static/songbook/html/songlist.html',
                controller: 'sbSonglistController',
                inMenu: false
            },

	   {
		caption: 'menuInstructions',
                url: '/instructions',
                templateUrl: '/static/songbook/html/instructions.html',
                controller: 'sbInstructionsController',
                inMenu: true
            }

        ])

        .constant('sbAccountsUrl', [
            'activate/:key',
            'login',
            'logout',
            'password/change',
            'password/change/done',
            'password/reset',
            'password/reset/confirm/:token/',
            'password/reset/complete',
            'password/reset/done',
            'register',
            'register/complete'
        ])

        .constant('sbTranslate', {
            en: {
                appName: 'songbook',
                signIn: 'sign in',
                signOut: 'sign out',
                loggedAs: 'logged as',
                menuHome: 'home',
                menuSongs: 'songs',
                menuSong: 'song',
                menuSonglists: 'song lists',
                menuSonglist: 'song list',
                allPdf: 'all songs PDF',
		menuInstructions: 'instructions',
                home: 'home',
                song: 'song',
                songs: 'songs',
                songlist: 'song list',
                songlists: 'song lists',
                performer: 'performer',
                composer: 'composer',
                year: 'year',
                availableSongs: 'available songs',
                songlistContent: 'songlist content',
                SonglistDropHere: 'Drag and drop songs here to create a songlist.',
                save: 'save',
                saved: 'saved',
                create: 'create',
                generatePDF: 'generate PDF' ,
		welcomeTitle: 'Welcome',
		welcome: 'Here will be cool welcome text',
		updates: 'Updates:',
		instructions: 'Instructions on typping songs'
            },
            pl: {
                appName: 'Śpiewnik', 
                signIn: 'zaloguj',
                signOut: 'wyloguj',
                loggedAs: 'zalogowano jako',
                menuHome: 'strona główna',
                menuSongs: 'piosenki',
                menuSong: 'piosenka',
                menuSonglists: 'listy piosenek',
                menuSonglist: 'lista piosenek',
                allPdf: 'PDF wszystkich piosenek',
		menuInstructions: 'instrukcje',
                home: 'strona główna',
                song: 'piosenka',
                songs: 'piosenki',
                songlist: 'lista piosenek',
                songlists: 'listy piosenek',
                performer: 'wykonawca',
                composer: 'kompozytor',
                year: 'rok',
                availableSongs: 'dostępne piosenki',
                songlistContent: 'zawartość listy piosenek',
                SonglistDropHere: 'Przeciągnij i upuść piosenki tutaj, by stworzyć listę piosenek.',
                save: 'zapisz',
                saved: 'zapisano',
                create: 'utwórz',
                generatePDF: 'generuj PDF' ,
		welcomeTitle: 'Witajcie',
		welcome: 'Tutuaj będzie ziomalskie powitanie',
		updates: 'Wiadomości:',
		instructions: 'Instrukcje wpisywania piosenki'

            }
        })

        .filter('sbUpperFirst', function () {
            return function upperFirst(input) {
                return input.charAt(0).toUpperCase() + input.slice(1);
            }
        });

}());
