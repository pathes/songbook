(function() {
    'use strict';

    angular.module('sb', ['ngResource', 'ngRoute', 'pascalprecht.translate', 'sbUtils', 'restangular'])

        .config(function ($interpolateProvider, $httpProvider, $locationProvider, $routeProvider,
                          $translateProvider, sbUrl, RestangularProvider) {

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
                songList: 'songs',
                performer: 'performer',
                composer: 'composer',
                year: 'year'
            });
            $translateProvider.translations('pl', {
                appName: 'Śpiewnik',
                menuHome: 'Strona główna',
                menuSongs: 'Piosenki',
                menuSong: 'Piosenka',
                home: 'strona główna',
                song: 'piosenka',
                songList: 'piosenki',
                performer: 'wykonawca',
                composer: 'kompozytor',
                year: 'rok'
            });
            $translateProvider.determinePreferredLanguage();

            RestangularProvider.setBaseUrl('/api');
            RestangularProvider.setRequestSuffix('\\');
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

        .controller('sbSongListController', function ($scope, sbSongScope) {
            sbSongScope.$watch('songs', function (songs) {
                $scope.songs = songs;
            });
        })

        .controller('sbSongController', function ($scope, $routeParams) {
            $scope.params = $routeParams;
        })

        .service('sbSongScope', function ($rootScope, Restangular) {
            var scope = $rootScope.$new();
            _.assign(scope, {
                songs: [],
                songlists: []
            });
            Restangular.one('song').getList().then(function (songs) {
                scope.songs = songs;
            });
            Restangular.one('songlist').getList().then(function (songlists) {
                scope.songlists = songlists;
            });
            return scope;
        })

        .directive('sbSonglist', function () {
            return {
                restrict: 'E',
                templateUrl: 'static/songbook/html/directives/songlist.html',
                scope: {
                    songs: '='
                },
                controller: function ($scope) {
                    $scope.categories = ['performer', 'composer', 'year'];
                    $scope.category = 'performer';
                    $scope.$watch('songs', function (songs) {
                        $scope.songsBy = {};
                        _.forEach($scope.categories, function (category) {
                            $scope.songsBy[category] = _.groupBy(songs, function (song) {
                                return song[category];
                            });
                        });
                    });
                }
            }
        });

}());
