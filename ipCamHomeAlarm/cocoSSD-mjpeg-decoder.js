
const node_modules = '/home/matteo/dev/node/node_modules';
const HTTP = require('http')
const fs = require('fs');
const tf = require(node_modules + '/@tensorflow/tfjs-node');
const coco = require(node_modules + '/@tensorflow-models/coco-ssd');
const Promise = require(node_modules + '/promise');
const { createCanvas, Image } = require(node_modules + '/canvas')
// ------------------------------------------------------------------------------

/**
 * Websocket server app
 *
 * Will use base64 return to the websocket clients and
 * in memory capturing without saving
 *
 */
"use strict";

var port = 9090;

var HTML_CONTENT = fs.readFileSync( __dirname + "/index.html" );

var WS = require( node_modules + '/ws' );

var WSS = new WS.Server({ port: 9091 });

// Broadcast to all.

WSS.broadcast = function broadcast( data ) {

    WSS.clients.forEach( function each( client ) {

        client.send( data );

    });

};

function setupHTTP() {

    var server = HTTP.createServer();

    server.on( "request", function( request, response ) {

        response.write( HTML_CONTENT );

        response.end();

    });

    server.listen( port );

}

renderPredictions = (predictions, frame) => {
  
  predictions.forEach(prediction => {  
  
   const text = prediction.score.toFixed(2).toString() + ':' + prediction.class;
   if(prediction.class != "person") { return }; 
   if(prediction.score < 0.80) { return }; 
   console.log(text);
   const date = new Date().toISOString();
   const dir = date.replace(/.........$/, '');
   if (!fs.existsSync(`./recordings/new/${dir}0`)){
       fs.mkdirSync(`./recordings/new/${dir}0`);
   }
   const fn = date.replace(dir, '0');
   fs.writeFileSync(`recordings/new/${dir}0/${fn}.jpg`, frame);
   // Bounding boxes's coordinates and sizes
   const x = prediction.bbox[0];
   const y = prediction.bbox[1];
   const width = prediction.bbox[2];
   const height = prediction.bbox[3];
// Draw the bounding
   ctx.strokeRect(x, y, width, height);  
   
   // Label background
   ctx.fillStyle = "#00FFFF";
   const textWidth = ctx.measureText(prediction.text).width;
   const textHeight = parseInt(font, 10); // base 10
   ctx.fillRect(x, y, textWidth + 14, textHeight + 14);

    // Write prediction class names
    // const x = prediction.bbox[0];
    // const y = prediction.bbox[1];  
    ctx.fillStyle = "#000000";
    ctx.fillText(text, x, y);   
   });
   
   // predictions.forEach(prediction => {
  };

const canvas = createCanvas(640, 360);
  canvas.width  = 640;
  canvas.height = 360;
  
const ctx = canvas.getContext('2d');
// Bounding box style
   ctx.strokeStyle = "#00FFFF";
   ctx.lineWidth = 2;
  // Fonts
  const font = "16px sans-serif";
  ctx.font = font;
  ctx.textBaseline = "top";
const img = new Image();

// Main
var tensor, predictions;
async function myMain() {
    const MjpegDecoder = require(node_modules + '/mjpeg-decoder');

    // create a decoder which delivers a JPEG frame
    // via the 'frame' event.
    const decoder = new MjpegDecoder(
      'http://192.168.1.242:81/videostream.cgi?loginuse=matteo&loginpas=oettam68'
      );
    
    decoder.on('frame', async (frame, seq) => {
    	// convert image from JPG to RGB
    	// console.log('converting JPG --> RGB');
    	img.src = frame;
    	ctx.beginPath();
    	ctx.clearRect(0, 0, 480, 360);
    	ctx.drawImage(img, 0, 0);
    	tensor = tf.browser.fromPixels(canvas);
	//tensor = tf.node.decodeImage(img);

	predictions = await net.detect(tensor);
	// console.log(seq + ' : ' + JSON.stringify(predictions));
	renderPredictions(predictions, frame);
    	await WSS.broadcast( canvas.toDataURL() );
	await tensor.dispose();
    });

    setupHTTP();
    console.log( "Visit localhost:9090" );

    console.log('loading Model');
    const net = await coco.load();
    await console.log('Starting ipCam...');
    await decoder.start();
}

myMain();
