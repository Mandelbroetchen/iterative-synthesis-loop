### Usecase
```
git clone https://github.com/Mandelbroetchen/iterative-synthesis-loop
cd ./iterative-synthesis-loop
echo MISTRAL_API_KEY=Your_MistralAI_API_key > .env
cd ./example
echo You_prompt > ./prompt-raw/description.md
python ../isl.py ./prompt-raw
```

