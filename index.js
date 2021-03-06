require('dotenv').config()
const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')

const app = express()
const port = process.env.PORT || 5000

app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.send('Welcome to the Jensen Chatbot for Zoom!')
})

app.get('/authorize', (req, res) => {
    res.redirect('https://zoom.us/launch/chat?jid=robot_' + process.env.zoom_bot_jid)
})

app.get('/support', (req, res) => {
    res.send('Contact jsingh8448@gmail.com for support.')
})

app.get('/privacy', (req, res) => {
    res.send('The Jensen Chatbot for Zoom stores username and user data relevant to the quizzes and tests.')
})

app.get('/terms', (req, res) => {
    res.send('By installing the Jensen Chatbot for Zoom, you are accept and agree to these terms...')
})

app.get('/documentation', (req, res) => {
    res.send('Try typing "kahoot kahoot_id" to start a kahoot game in Zoom.!')
})

app.get('/zoomverify/verifyzoom.html', (req, res) => {
    res.send(process.env.zoom_verification_code)
})

app.post('/Jensen', (req, res) => {
    getChatbotToken()

    function getMessage(chatbotToken) {

        var errors = [
            {
                'type': 'section',
                'sidebar_color': '#D72638',
                'sections': [{
                    'type': 'message',
                    'text': 'Error getting message from Jensen.'
                }]
            }
        ]
        sendChat(errors, chatbotToken)

    }

    function getChatbotToken() {
        request({
            url: `https://api.zoom.us/oauth/token?grant_type=client_credentials`,
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + Buffer.from(process.env.zoom_client_id + ':' + process.env.zoom_client_secret).toString('base64')
            }
        }, (error, httpResponse, body) => {
            if (error) {
                console.log('Error getting chatbot_token from Zoom.', error)
            } else {
                body = JSON.parse(body)
                getMessage(body.access_token)
            }
        })
    }

    function sendChat(chatBody, chatbotToken) {
        request({
            url: 'https://api.zoom.us/v2/im/chat/messages',
            method: 'POST',
            json: true,
            body: {
                'robot_jid': process.env.zoom_bot_jid,
                'to_jid': req.body.payload.toJid,
                'account_id': req.body.payload.accountId,
                'content': {
                    'head': {
                        'text': '/Jensen ' + req.body.payload.cmd
                    },
                    'body': chatBody
                }
            },
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + chatbotToken
            }
        }, (error, httpResponse, body) => {
            if (error) {
                console.log('Error sending chat.', error)
            } else {
                console.log(body)
            }
        })
    }

})

app.post('/deauthorize', (req, res) => {
    if (req.headers.authorization === process.env.zoom_verification_token) {
        res.status(200)
        res.send()
        request({
            url: 'https://api.zoom.us/oauth/data/compliance',
            method: 'POST',
            json: true,
            body: {
                'client_id': req.body.payload.client_id,
                'user_id': req.body.payload.user_id,
                'account_id': req.body.payload.account_id,
                'deauthorization_event_received': req.body.payload,
                'compliance_completed': true
            },
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + Buffer.from(process.env.zoom_client_id + ':' + process.env.zoom_client_secret).toString('base64'),
                'cache-control': 'no-cache'
            }
        }, (error, httpResponse, body) => {
            if (error) {
                console.log(error)
            } else {
                console.log(body)
            }
        })
    } else {
        res.status(401)
        res.send('Unauthorized request to Jensen Chatbot for Zoom.')
    }
})

app.listen(port, () => console.log(`Jensen Chatbot for Zoom listening on port ${port}!`))
