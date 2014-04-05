(function() {
    'use strict';

    angular.module('sb', ['ngResource', 'ngRoute', 'pascalprecht.translate', 'sbUtils'])

        .config(function ($interpolateProvider, $httpProvider, $locationProvider, $routeProvider,
                          $translateProvider, sbUrl) {

            $interpolateProvider.startSymbol('[[');
            $interpolateProvider.endSymbol(']]');
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $locationProvider.html5Mode(true);

            _.forEach(sbUrl, function (menuItem) {
                $routeProvider.when(menuItem.url, _.pick(menuItem, ['templateUrl', 'controller']));
            });
            $routeProvider.otherwise({
                redirectTo: '/'
            });

            $translateProvider.translations('en', {
                appName: 'Songbook',
                menuHome: 'Home',
                menuSongs: 'Songs',
                menuSong: 'Song',
                home: 'home',
                song: 'song',
                songList: 'songs'
            });
            $translateProvider.translations('pl', {
                appName: 'Śpiewnik',
                menuHome: 'Strona główna',
                menuSongs: 'Piosenki',
                menuSong: 'Piosenka',
                home: 'strona główna',
                song: 'piosenka',
                songList: 'piosenki'
            });
            $translateProvider.determinePreferredLanguage();
        })

        .controller('sbBaseController', function ($scope, $location, $translate, sbUrl) {
            _.assign($scope, {
                menuItems: _.filter(sbUrl, 'inMenu'),
                menuItemActive: function (menuItem) {
                    // Special case for '/'
                    if (menuItem.url === '/') {
                        if ($location.path() === '/') {
                            return 'active';
                        }
                    } else if ($location.path().substr(0, menuItem.url.length) === menuItem.url) {
                        return 'active';
                    }
                    return '';
                },
                languages: ['en', 'pl'],
                changeLanguage: function (language) {
                    $translate.use(language);
                },
                languageActive: function (language) {
                    return $translate.use() === language ? 'active' : '';
                }
            });
        })

        .controller('sbHomeController', function () {
        })

        .controller('sbSongListController', function () {
        })

        .controller('sbSongController', function ($scope, $routeParams) {
            $scope.params = $routeParams;
        });

}());
