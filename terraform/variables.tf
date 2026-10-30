variable "aws_profile" {
  description = "AWS CLI profile used for all API calls."
  type        = string
  default     = "tamdo"
}

variable "aws_region" {
  description = "Region for ECR, S3 and Lambda. CloudFront is global."
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Short name used as a prefix for every resource."
  type        = string
  default     = "mbti"
}

variable "environment" {
  description = "Deployment stage, e.g. dev or prod."
  type        = string
  default     = "dev"
}

variable "image_tag" {
  description = "Tag of the backend image in ECR. The Lambda is pinned to this tag's digest, so pushing a new tag and applying redeploys it."
  type        = string
  default     = "bootstrap"
}

variable "lambda_memory_mb" {
  description = "Memory for the backend Lambda."
  type        = number
  default     = 512
}

variable "lambda_timeout_s" {
  description = "Timeout for the backend Lambda. CloudFront's origin read timeout is 30s, so going higher has no effect for API calls."
  type        = number
  default     = 30
}

variable "lambda_architecture" {
  description = "Lambda CPU architecture; must match the platform the image was built for."
  type        = string
  default     = "x86_64"

  validation {
    condition     = contains(["x86_64", "arm64"], var.lambda_architecture)
    error_message = "lambda_architecture must be x86_64 or arm64."
  }
}

variable "cors_allow_origins" {
  description = "Extra browser origins allowed to call the API cross-origin. Not needed for the CloudFront-served frontend."
  type        = list(string)
  default     = []
}

variable "enable_api_docs" {
  description = "Serve Swagger UI at /api/docs. Off by default: it needs CDN scripts the CloudFront CSP blocks, and it publishes the API schema."
  type        = bool
  default     = false
}

variable "cloudfront_price_class" {
  description = "CloudFront price class. PriceClass_200 includes Asia edge locations."
  type        = string
  default     = "PriceClass_200"
}
