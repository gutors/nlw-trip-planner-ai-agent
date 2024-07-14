# Use the AWS base image for Python 3.12
FROM public.ecr.aws/lambda/python:3.12

# Install build-essential compiler and tools
RUN microdnf update -y && microdnf install -y gcc-c++ make

# Copy requirements.tsx
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}

# Install packages
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy function code
COPY ./src/travelAgent.py ${LAMBDA_TASK_ROOT}

# Set the permissions to make the file executable
RUN chmod +x ${LAMBDA_TASK_ROOT}/travelAgent.py

# Set the CMD to your handler
CMD ["travelAgent.lambda_handler"]