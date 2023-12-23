# lambda-logging-example

Example of lambda logging behavior.


## Building the image

Use `docker build`.

```sh
docker build -t example-lambda .
```


## Logging into ECR

We use different accounts for ECR images and Lambda deployments for ease of
image reuse across accounts. We use AWS profiles in conjunction with SSO
to facilitate CLI usage across accounts.

Your setup will likely differ.

```
aws --profile lettuce-images ecr get-login-password \
    | docker login -u AWS --password-stdin 607442316485.dkr.ecr.us-east-2.amazonaws.com
```


## Publishing the image

Use `docker` to `build` an image the expected name and push it to ECR.

```sh
docker build --platform linux/x86_64 -t 607442316485.dkr.ecr.us-east-2.amazonaws.com/example-lambda:latest .
docker push 607442316485.dkr.ecr.us-east-2.amazonaws.com/example-lambda:latest
```


# Updating the function

Ensure that the Lambda function is using this image.

```sh
aws --profile lettuce-dev lambda update-function-code \
  --function-name example \
  --image-uri 607442316485.dkr.ecr.us-east-2.amazonaws.com/example-lambda:latest

aws --profile lettuce-dev lambda wait function-updated \
  --function-name example
```
