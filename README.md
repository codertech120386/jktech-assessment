### ABOUT THE APPLICATION

- The application is coded in FastAPI using Python 3.12 as the python version.
- It uses PostgreSQL 15 as the Database
- For llama3 I am using ollama which is deployed as part of the parent image which is used by this application as the
  base image
- Application is deployed to AWS ECS.
- I have used CircleCI CICD Pipeline to deploy to ECS.
- Application swagger documentation can be accessed on https://jktech.learnindiancuisine.com/docs
- Source code for the application is hosted on Github on url :- https://github.com/codertech120386/jktech-assessment
- Application has a /status endpoint which is used by load balancer for performing health check.

### STEPS TO ACCESS THE APPLICATION

- Please visit https://jktech.learnindiancuisine.com/docs
- First you need to register a user so please access the /api/v1/auth/register endpoint and register a user.
- You will receive a token in the response json so please copy that and click on Authorize at the top right of the page
  or any lock in the below apis and add that token and click Authorize. You will now be an authenticated user.
- All the routes except Authorization are auth protected, so you need to authenticate yourself to access it.
- Once you have a user you can use the /api/v1/auth/register endpoint in future to get the token.

### AI routes

- to generate summary for the content you need to use /api/v1/generate-summary endpoint.

**Please Note** :- Llama model takes some time to give the response so please be patient.

- There are 2 ways to train the model.

1) A synthetic dataset can be used which is deployed to s3 and model can be trained on that csv.
2) I have created an endpoint called /api/v1/books/train-model and that will fetch contents from the db and model will
   be trained on that data.

**Please Note** :- I have created pickle files and stored them on s3 which when model is trained.

- For recommendations, I have the endpoint /api/v1/recommendations which pulls the pickle files from s3 and generates
  recommendations.