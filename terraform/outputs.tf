output "cloudfront_domain_name" {
  description = "Public HTTPS URL of the application."
  value       = "https://${aws_cloudfront_distribution.main.domain_name}"
}

output "cloudfront_distribution_id" {
  description = "Distribution ID, used for cache invalidations after a frontend deploy."
  value       = aws_cloudfront_distribution.main.id
}

output "ecr_repository_url" {
  description = "ECR repository URL for the backend image."
  value       = aws_ecr_repository.backend.repository_url
}

output "s3_bucket_name" {
  description = "Bucket to sync the frontend build into."
  value       = aws_s3_bucket.frontend.bucket
}

output "lambda_function_name" {
  description = "Backend Lambda function name."
  value       = aws_lambda_function.backend.function_name
}
