// set the load function name: graphLoad
// var wfConfigDiv = document.getElementById("workflowId");
// var inputArr = wfConfigDiv.getElementsByTagName("input");
// var functionElem = inputArr[1];
// functionElem.setAttribute('value', 'graphLoad');
// set some flags
var frameLoadedFlag = false;
var initalPaintFlag = false;
var RESPONSE_TIME_LIMIT = 6000;
var responseTimeCounter = 0;
var wfCompletedFlag = false;


// functions 
function reset() {
  frameLoadedFlag = false;
  initalPaintFlag = false;
  RESPONSE_TIME_LIMIT = 6000;
  responseTimeCounter = 0;
  wfCompletedFlag = false;

  var graphDiv = document.getElementById("workflow-graph");
  graphDiv.innerHTML = '';
}

function setIframeSrc()
{        
 var iframeContainer = document.getElementById("iframeContainer");
 var iframeDiv = document.getElementById("testFrame");
 if(iframeDiv != undefined ) {
     iframeContainer.removeChild(iframeDiv);
 }
 var apiPrefix = "http://localhost:8600/#/workflow/id/";
 var wfConfigDiv = document.getElementById("workflowId");
 var inputArr = wfConfigDiv.getElementsByTagName("input");
 var idElem = inputArr[0];
 var workflowId = idElem.getAttribute("value");
 var apiUrl = apiPrefix + workflowId;
 var iframeDiv = "<iframe id=\"testFrame\" width=\"0\" height=\"0\" style=\"display:none\" src=\"" + apiUrl + "\"></iframe>";
 iframeContainer.innerHTML = iframeDiv;

 frameLoadedFlag = false;
}

function initialPaint() {
  var iframe = document.getElementById("testFrame");
  var content = iframe.contentWindow.document.getElementById("graph-ui-content").cloneNode(true); 
  content.id = "graph-ui-content-1";
  var graphDiv = document.getElementById("workflow-graph");
  graphDiv.appendChild(content); 

  initalPaintFlag = true;
} 
function initialPaintWFGraph() {
 console.log("start to initial paint");
 setIframeSrc();  
 var iframe = document.getElementById("testFrame");
 if (iframe.attachEvent) {
   iframe.attachEvent("onload", function(){
     window.setTimeout(function(){
        frameLoadedFlag = true;
        initialPaint();
        console.log("finish to initial paint");
     }, 1000);
   });
 } else {
  iframe.onload = function(){
    window.setTimeout(function(){
        frameLoadedFlag = true;
        initialPaint();
        console.log("finish to initial paint");
     }, 1000);
   }
 }
}


function repaint() {
 var iframe = document.getElementById("testFrame");
 var newContent = iframe.contentWindow.document.getElementById("graph-ui-content").cloneNode(true); 
 var newNodes = newContent.getElementsByClassName("node");
 
 var oldContent = document.getElementById("graph-ui-content-1");
 var oldNodes = oldContent.getElementsByClassName("node");
 
 if(newNodes.length > oldNodes.length) {
  console.log("execute in new > old");
    newContent.id = "graph-ui-content-1";
    var graphDiv = document.getElementById("workflow-graph"); 
    graphDiv.innerHTML = '';
    graphDiv.appendChild(newContent);
 } 
 else if(newNodes.length == oldNodes.length) {
    console.log("execute in new = old");
    for(var i = 0; i < newNodes.length; i++)
    {
      var newGraph = newNodes[i].children[0];
      var newGraphStyle = newGraph.getAttribute("style");

      var oldGraph = oldNodes[i].children[0];
      var oldGraphStyle = oldGraph.getAttribute("style");
      if(newGraphStyle != oldGraphStyle) {
        oldGraph.setAttribute("style", newGraphStyle);
      }
      var newText = newNodes[i].getElementsByTagName("text")[0];
      var newTextStyle = newText.getAttribute("style");
      var oldText = oldNodes[i].getElementsByTagName("text")[0];
      var oldTextStyle = oldText.getAttribute("style");
      if(oldTextStyle != newTextStyle) {
        oldText.setAttribute("style", newTextStyle);
      }
      if(i == (newNodes.length - 1) && newGraphStyle == 'stroke: #48a770; fill: #48a770') {
          wfCompletedFlag = true;
      }
    } 
 }
 else {
  console.log("execute in new < old");
 }
}

function repaintWFGraph() {
 setIframeSrc();  
 var iframe = document.getElementById("testFrame");
 if (iframe.attachEvent) {
   iframe.attachEvent("onload", function(){
     window.setTimeout(function(){
        frameLoadedFlag = true;
        repaint();
     }, 1000);
   });
 } else {
  iframe.onload = function(){
    window.setTimeout(function(){
        frameLoadedFlag = true;
        repaint();
     }, 1000);
   }
 } 
}      

function graphLoad(){
  console.log("load function activate");
  reset();

  initialPaintWFGraph();
  var intervalTime = 1000;
  var intervalId = window.setInterval(function() {
    if(wfCompletedFlag) {
      window.clearInterval(intervalId);
      getWFOutput();
    }
    if(!initalPaintFlag) {
      if(responseTimeCounter > RESPONSE_TIME_LIMIT) {
        initialPaintWFGraph();
        responseTimeCounter = 0;
      }
    } else {
      if(frameLoadedFlag || responseTimeCounter > RESPONSE_TIME_LIMIT) {
        repaintWFGraph();
        responseTimeCounter = 0;
      }
    }
    responseTimeCounter += intervalTime;
  }, intervalTime);
}

function getWFOutput() {
  console.log("getWFOutput active");
  var wfConfigDiv = document.getElementById("workflowId");
  var inputArr = wfConfigDiv.getElementsByTagName("input");
  var idElem = inputArr[0];
  var workflowId = idElem.getAttribute("value");
  console.log("getWFOutput active");
  var url = "http://localhost:8600/workflow_server/api/workflow/" + workflowId + "?includeTasks=false";
  $.ajax({
      url: url,
      method: "GET",
      success: function(data) {
          console.log("get output:");
          console.log(data);
          var fData = {};
          fData['output'] = data['output'];
          fData['status'] = data['status'];
          var createTime = timestampToTime(data['createTime']);
          fData['createTime'] = createTime;
          var endTime = timestampToTime(data['endTime']);
          fData['endTime'] = endTime;
          console.log(fData);
          fData = JSON.stringify(fData, null, "    ");
          console.log(fData);
          var outputElem = document.getElementById("workflow-output");
          outputElem.innerHTML = fData;
      }
  });
}