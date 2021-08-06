# review_sentiment_app
Review Sentiment Analysis App

This is a flask app deployed on EC2 instance. Weight and Biases is used to track additional metrics.  Deployment steps are as below:
1. Create EC2 instance (t2.medium)
2. Add security groups to allow intended inbound and outbound traffic
3. Develop the flask app 
4. Set WANDB key as environment variable with `export WANDB_KEY=[api_key]`
5. run the app on the EC2 instance with `. run.sh` 
