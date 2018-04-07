/**
 * Copyright 2017 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 import sendText from './demoFunctions.js';
 import $ from 'jquery';
  "use strict";

  var ENTER_KEY_CODE = 13;
  var queryInput, resultDiv, accessTokenInput;

  export function init(resultElem) {
    resultDiv = resultElem;
    queryInput = $("#q").get(0);
    queryInput.addEventListener("keydown", queryInputKeyDown);
  }
  export function queryInputKeyDown(event) {
    if (event.which !== ENTER_KEY_CODE) {
      return;
    }
    var value = queryInput.value;
    queryInput.value = "";
    if (value ==="") {
      return;
    }

    createQueryNode(value);
    var responseNode = createResponseNode();

    sendText(value)
      .then(function(response) {
        var result;
        try {
          result = response.result.fulfillment.speech
        } catch(error) {
          result = "";
        }
        //setResponseJSON(response);
        setResponseOnNode(result, responseNode);
      })
      .catch(function(err) {
        //setResponseJSON(err);
        setResponseOnNode("Something goes wrong", responseNode);
      });
  }

  function createQueryNode(query) {
    var node = document.createElement('div');
    node.className = "clearfix left-align left card-panel light-blue darken-4";
    node.innerHTML = query;
    resultDiv.insertBefore(node, resultDiv.firstChild);
      $( "#result div:last-child" ).delay(3000).fadeOut( "slow", function() {
        $(this).remove();
        $( "#result div:last-child" ).delay(3000).fadeOut( "slow", function() {
          $(this).remove();
        })
      });
  }

  function createResponseNode() {
    var node = document.createElement('div');
    node.className = "clearfix right-align right card-panel blue-text text-darken-2 hoverable";
    node.innerHTML = "...";
    resultDiv.insertBefore(node, resultDiv.firstChild);
    return node;
  }

  function setResponseOnNode(response, node) {
    node.innerHTML = response ? response : "[empty response]";
    node.setAttribute('data-actual-response', response);
  }

  /*
  function setResponseJSON(response) {
    var node = document.getElementById("jsonResponse");
    node.innerHTML = JSON.stringify(response, null, 2);
  }

  function sendRequest() {

  }
  */
;
