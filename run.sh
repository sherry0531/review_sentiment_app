docker build -t app .
docker run --rm \
	-e WANDB_KEY=$WANDB_KEY \
	-p 5000:5000 app
	
