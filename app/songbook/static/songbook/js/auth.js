(function() {
    'use strict';

    // Based on http://richardtier.com/2014/03/15/authenticate-using-django-rest-framework-endpoint-and-angularjs/ .
    angular.module('sbAuth', ['ngResource'])

        .factory('sbAuth', function ($resource, $rootScope) {
            function addAuthHeader(data, headersGetter){
                // As per HTTP authentication spec [1], credentials must be
                // encoded in base64. Lets use window.btoa [2].
                // [1] https://tools.ietf.org/html/rfc2617
                // [2] https://developer.mozilla.org/en-US/docs/Web/API/Window.btoa
                var headers = headersGetter();
                headers['Authorization'] = 'Basic ' + btoa(data.username + ':' + data.password);
            }

            var Auth = $resource('/api/auth\\/', {}, {
                login: {method: 'POST', transformRequest: addAuthHeader},
                logout: {method: 'DELETE'}
            });

            var scope = $rootScope.$new();
            _.assign(scope, window.auth || {});
            _.assign(scope, {
                login: function (credentials) {
                    Auth.login(credentials).$promise
                        .then(function (authData) {
                            scope.id = authData.id;
                            scope.username = authData.username;
                            scope.error = undefined;
                        })
                        .catch(function (error) {
                            scope.error = error.data.detail;
                        });
                },
                logout: function () {
                    Auth.logout(function() {
                        scope.id = undefined;
                        scope.username = undefined;
                    });
                }
            });

            return scope;
        })

}());
