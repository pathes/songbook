(function() {
    'use strict';

    angular.module('sb', ['ngResource', 'ngRoute', 'pascalprecht.translate', 'sbAuth', 'sbUtils', 'restangular'])

        .config(function ($interpolateProvider, $httpProvider, $locationProvider, $routeProvider,
                          $translateProvider, sbTranslate, sbUrl, sbAccountsUrl, RestangularProvider) {

            $interpolateProvider.startSymbol('[[');
            $interpolateProvider.endSymbol(']]');
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $locationProvider.html5Mode(true);

            _.forEach(sbUrl, function (menuItem) {
                $routeProvider.when(menuItem.url, _.pick(menuItem, ['templateUrl', 'controller']));
            });
            // Allow django-registration templates to be rendered.
            $routeProvider.when('/accounts/:whatever/', {});
            $routeProvider.when('/accounts/:whatever/:whatever2/', {});
            $routeProvider.otherwise({
                redirectTo: '/' // TODO 404 handling
            });

            _.forIn(sbTranslate, function (translation, language) {
                $translateProvider.translations(language, translation);
            });
            $translateProvider.determinePreferredLanguage();

            RestangularProvider.setBaseUrl('/api');
            RestangularProvider.setRequestSuffix('/');
        })

        .controller('sbBaseController', function ($scope, $http, $location, $route, $translate, sbAuth, sbUrl) {
            _.assign($scope, {
                username: window.username,
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
                    $http.post('/api/locale/', {locale: language});
                },
                languageActive: function (language) {
                    return $translate.use() === language ? 'active' : '';
                },
                auth: sbAuth
            });
            $scope.$on('$routeChangeSuccess', function () {
                if (!/\/accounts/.test($location.path())) {
                    var staticContent = document.getElementById('static-content');
                    if (staticContent) {
                        staticContent.remove();
                    }
                }
            });
        })

        .controller('sbAccountsController', function () {
        })

        .controller('sbHomeController', function ($scope, sbArticleScope) {
            sbArticleScope.$watch('articles', function (articles) {
                $scope.articles = articles;
            });
        })

        .controller('sbSongListController', function ($scope, sbSongScope) {
            sbSongScope.$watch('songs', function (songs) {
                $scope.songs = songs;
            });
        })

        .controller('sbSongController', function ($scope, $routeParams, sbSongScope) {
            sbSongScope.$watch('songs', function (songs) {
                $scope.song = _.find(songs, {pk: +$routeParams.songId});
                if (songs && !$scope.song) {
                    // TODO song not found, show error message
                    console.error('Song not found!');
                }
            });
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

        .service('sbArticleScope', function ($rootScope, Restangular) {
            var scope = $rootScope.$new();
            _.assign(scope, {
                articles: []
            });
            Restangular.one('article').getList().then(function (articles) {
                scope.articles = articles;
            });
            return scope;
        })

        .directive('sbSonglist', function () {
            return {
                restrict: 'E',
                templateUrl: 'static/songbook/html/directives/songlist.html',
                scope: {
                    songs: '=',
                    linked: '&'
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
