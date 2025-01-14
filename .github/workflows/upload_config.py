name: Update Config

on:
  workflow_dispatch:
    inputs:
      config:
        description: 'JSON Configuration'
        required: true
        type: string

jobs:
  upload:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    
    - name: Upload Config
      env:
        CONFIG_JSON: ${{ inputs.config }}
        FTP_HOST: ${{ secrets.FTP_HOST }}
        FTP_USER: ${{ secrets.FTP_USER }}
        FTP_PASS: ${{ secrets.FTP_PASS }}
      run: python upload_config.py
