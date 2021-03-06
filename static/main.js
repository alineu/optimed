(function () {

  'use strict';

  angular.module('OptiMedApp', [])

  .controller('OptiMedController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $scope.submitButtonText = 'Submit';
    $scope.loading = false;
    $scope.urlerror = false;

    $scope.getResults = function() {

      $log.log('test');

      // get the user conditions (URL) from the input
      var userInput = $scope.url;

      // fire the API request
      $http.post('/start', {'url': userInput}).
        success(function(results) {
          $log.log(results);
          getBestMed(results);
          $scope.optimed_search_results = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Loading...';
          $scope.urlerror = false;
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    function getBestMed(jobID) {

      var timeout = '';

      var poller = function() {
        // fire another request
        $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $scope.loading = false;
              $scope.submitButtonText = "Submit";
              $scope.optimed_search_results = data;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          }).
          error(function(error) {
            $log.log(error);
            $scope.loading = false;
            $scope.submitButtonText = "Submit";
            $scope.urlerror = true;
          });
      };

      poller();

    }

  }])
.directive('wordCountChart', ['$parse', function ($parse) {
    return {
      restrict: 'E',
      replace: true,
      template: '<div id="chart"></div>',
      link: function (scope) {
        scope.$watch('optimed_search_results', function() {
          d3.select('#chart').selectAll('*').remove();
          var data = scope.optimed_search_results;
          for (var item in data) {
            d3.select('#chart')
              .append('div')
              .selectAll('div')
              .data(item[0])
              .enter()
              .append('div')
              .style('width', function() {
                return (data[item] * 20) + 'px';
              })
              .text(function(d){
                return item;
              });
          }
        }, true);
      }
     };
  }]);
  
angular.module('OptiMedAppRadar', [])
.controller('OptiMedControllerRadar', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $scope.submitButtonText = 'Submit';
    $scope.loading = false;
    $scope.urlerror = false;

    $scope.getMyResults = function() {

      $log.log('test');

      // get the user conditions (URL) from the input
      var userInput = $scope.url;

      // fire the API request
      $http.post('/start', {'url': userInput}).
        success(function(results) {
          $log.log(results);
          getBestMed(results);
          $scope.optimed_search_results_radar = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Loading...';
          $scope.urlerror = false;
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    function getBestMed(jobID) {

      var timeout = '';

      var poller = function() {
        // fire another request
        $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $scope.loading = false;
              $scope.submitButtonText = "Submit";
              $scope.optimed_search_results_radar = data;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          }).
          error(function(error) {
            $log.log(error);
            $scope.loading = false;
            $scope.submitButtonText = "Submit";
            $scope.urlerror = true;
          });
      };

      poller();

    }

  }])

  .directive('wordCountChartRadar', ['$parse', function ($parse) {
    return {
      restrict: 'E',
      replace: true,
      template: '<div id="radarchart"></div>',
      link: function (scope) {
        scope.$watch('optimed_search_results', function() {
          d3.select('#radarchart').selectAll('*').remove();
          var data = scope.optimed_search_results;
          for (var item in data) {
            d3.select('#radarchart')
              .append('div')
              .selectAll('div')
              .data(item[0])
              .enter()
              .append('div')
              .style('width', function() {
                return (data[item] * 20) + 'px';
              })
              .text(function(d){
                return item;
              });
          }
        }, true);
      }
     };
  }]);
  

}());
