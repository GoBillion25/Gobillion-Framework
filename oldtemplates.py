bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://gobillion-images-production.s3.ap-south-1.amazonaws.com/icons/customerSupport.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://gobillion-images-production.s3.ap-south-1.amazonaws.com/question.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

css = '''
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    max-width: 80%;
}

.chat-message.user {
    background-color: #f0f0f0;
    color: #000;
    justify-content: flex-end;
    align-self: flex-end;
    margin-left: auto; /* This will push the user message to the right */
}

.chat-message.bot {
    background-color: #e0e0e0;
    color: #000;
    justify-content: flex-start;
    align-self: flex-start;
    margin-right: auto; /* This will push the bot message to the left */
}

.chat-message .avatar {
    width: 20%;
}

.chat-message .avatar img {
    max-width: 40px;
    max-height: 40px;
    border-radius: 50%;
    object-fit: cover;
}
.stTextInput {
    margin-top: auto;
    transform: translateY(55vh);
    display: inline-block;
}
.chat-message .message {
    width: 80%;
    padding: 0 1rem;
    border-radius: 0.5rem; /* Rounded corners for the message */
}
</style>
'''
