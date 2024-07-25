from setuptools import setup, find_packages

setup(
    name='nlp_for_recruitment',
    version='1.0',
    author='Anas Aberchih',
    author_email='anas.aberchih1@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pypdf',
        'langchain',
        'langchain-community,'
        'chromadb,'
        'numpy',
        'scikit-learn',
        'pytest'
        'python-dotenv,'
        'transformers,'
        'FlagEmbedding',
        'einops',
        'joblib',
        'torch',
        'onnx',
        'onnxruntime',
        'cohere',
        'groq',
    ]
),