### Setup
```
# Clone project
git clone https://github.com/Mandelbroetchen/iterative-synthesis-loop

# Copy template and ISL
cp iterative-synthesis-loop/project-templates/code-project YOUR_PROJECT_NAME
cp iterative-synthesis-loop/ISL YOUR_PROJECT_NAME/ISL
cd YOUR_PROJECT_NAME

# API key
echo MISTRAL_API_KEY=YOUR_MISTRAL_AI_API_KAY > .env
# If you have other providers, edit the following files:
# requirements/configs/api.json
# specifications/configs/api.json
# code-raw/configs/api.json
# code-final/configs/api.json
```
### Workflow

The project has 4 folders `requirements`, `specifications`, `code-raw`, `code-final`, each having a `contents` subfolder. In `requirements/contents/product-requirements.md`, enter your initial prompt and compile with

```
python -m ISL.compile requirements
```
The folder `specifications/contents` will update according to your prompt. You can continue to compile with
```
python -m ISL.compile specifications
```
The folder `code-raw/contents` will update. 

