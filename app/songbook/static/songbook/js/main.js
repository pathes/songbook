(function() {
    'use strict';

    angular.module('sb', [
            'ngDragDrop', 'ngResource', 'ngRoute', 'pascalprecht.translate', 'sbAuth', 'sbUtils', 'restangular'
        ])

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
            $routeProvider.otherwise({
                redirectTo: '/' // TODO 404 handling
            });

            _.forIn(sbTranslate, function (translation, language) {
                $translateProvider.translations(language, translation);
            });
            $translateProvider.determinePreferredLanguage();

            RestangularProvider.setBaseUrl('/api');
            RestangularProvider.setRequestSuffix('/');
            RestangularProvider.setRestangularFields({id: "pk"});
        })

        .controller('sbBaseController', function ($scope, $http, $location, $route, $translate, sbAuth, sbUrl) {
            _.assign($scope, {
                menuItems: _.filter(sbUrl, 'inMenu'),
                menuItemActive: function (menuItem) {
                    // Special case for '/'
                    if (menuItem.url === '/') {
                        if ($location.path() === '/') {
                            return 'active';
                        }
                    } else if (($location.path() + '/').substr(0, menuItem.url.length + 1) === menuItem.url + '/') {
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

        .controller('sbSongsController', function ($scope, $location, sbAuth, Restangular) {
            Restangular.all('song').getList().then(function (songs) {
                $scope.songs = songs;
            });
            _.assign($scope, {
                authenticated: function () {
                    return !!sbAuth.id;
                },
                create: function () {
                    Restangular.all('song').post({
                        author: sbAuth.id,
                        title: '…',
                        content: '…'
                    }).then(function (newSong) {
                        $location.path('/song/' + newSong.pk);
                    });
                }
            });
        })

        .controller('sbSongController', function ($scope, $routeParams, $location, sbAuth, Restangular) {
            Restangular.one('song', +$routeParams.songId).get().then(
                function (song) {
                    _.assign($scope, {
                        song: song,
                        editing: function () {
                            return sbAuth.id === song.author;
                        }
                    });
                },
                function () {
                    $location.path('/song');
                }
            );
            _.assign($scope, {
                params: $routeParams,
                saved: true,
                save: function () {
                    $scope.song.put().then(function () {
                        $scope.saved = true;
                    });
                }
            });
        })

        .controller('sbSonglistsController', function ($scope, sbAuth, $location, Restangular) {
            Restangular.all('songlist').getList().then(function (songlists) {
                $scope.songlists = songlists;
            });
            _.assign($scope, {
                authenticated: function () {
                    return !!sbAuth.id;
                },
                create: function () {
                    Restangular.all('songlist').post({
                        author: sbAuth.id,
                        title: '…',
                        is_public: true,
                        songs: []
                    }).then(function (newSonglist) {
                        $location.path('/songlist/' + newSonglist.pk);
                    });
                }
            });
        })

        .controller('sbSonglistController', function ($scope, $location, $routeParams, sbAuth, Restangular) {
            // Send requests first
            var songlistRequest = Restangular.one('songlist', +$routeParams.songlistId).get();
            var songsRequest = Restangular.all('song').getList();
            // then add callbacks
            songlistRequest.then(
                function (songlist) {
                    songsRequest.then(
                        function (songs) {
                            _.assign($scope, {
                                songs: songs,
                                songlist: songlist,
                                songlistSongs: _.map(songlist.songs, function (songId) {
                                    return _.find(songs, {pk: songId});
                                }),
                                editing: function () {
                                    return sbAuth.id === songlist.author;
                                }
                            });
                        }
                    );
                },
                function () {
                    $location.path('/songlist');
                }
            );

            var lastAdded;

            _.assign($scope, {
                params: $routeParams,
                saved: true,
                dropAddSong: function ($event, $index, $data) {
                    // If $index not provided, add song to end.
                    if ($index === undefined) {
                        $index = Infinity;
                    }
                    // Used in drag'n'drop.
                    $scope.songlistSongs.splice($index, 0, $data);
                    $scope.saved = false;
                    lastAdded = $index;
                },
                dropRemoveSong: function ($event, $index) {
                    if (lastAdded < $index) {
                        $index++;
                    }
                    $scope.songlistSongs.splice($index, 1);
                    $scope.saved = false;
                },
                removeSong: function ($index) {
                    // Used for removing song by pressing "×" button.
                    $scope.songlistSongs.splice($index, 1);
                    $scope.saved = false;
                },
                save: function () {
                    $scope.songlist.songs = _.map($scope.songlistSongs, function (song) {
                        return song.pk;
                    });
                    $scope.songlist.put().then(function () {
                        $scope.saved = true;
                    });
                }
            });
        })

        .service('sbArticleScope', function ($rootScope, Restangular) {
            var scope = $rootScope.$new();
            _.assign(scope, {
                articles: []
            });
            Restangular.all('article').getList().then(function (articles) {
                scope.articles = articles;
            });
            return scope;
        })

        .directive('sbPlainSongs', function () {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: '/static/songbook/html/directives/plain-songs.html',
                scope: {
                    songs: '=',
                    linked: '=',
                    draggable: '='
                }
            }
        })

        .directive('sbEditableSongs', function () {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: '/static/songbook/html/directives/editable-songs.html',
                scope: {
                    songs: '=',
                    linked: '=',
                    dropAddSong: '=',
                    dropRemoveSong: '=',
                    removeSong: '='
                }
            }
        })

        .directive('sbFilteredSongs', function () {
            return {
                restrict: 'E',
                templateUrl: '/static/songbook/html/directives/filtered-songs.html',
                scope: {
                    songs: '=',
                    linked: '=',
                    draggable: '='
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
