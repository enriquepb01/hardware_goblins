const functions = require("firebase-functions");
const admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);

const db = admin.firestore();

const mqtt = require('mqtt');

// // Create and deploy your first functions
// // https://firebase.google.com/docs/functions/get-started
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//   functions.logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

exports.serveArray = functions
    .region('us-west2')
    .https.onRequest((request, response) => {
        db.collection('filters').doc('current')
        .get().then((snapshot) => 
            response.send(snapshot.data().filter)
        )
    })

exports.sendMqtt = functions
    .region('us-west2')
    .https.onCall((data, context) => {
        let client = mqtt.Client;

        client = mqtt.connect("mqtt://eclipse.usc.edu:11000");

        client.on('connect', () => console.log('connncete'))

        client.publish('goblin/test', data.message)
    })