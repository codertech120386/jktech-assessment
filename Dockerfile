FROM kiddodhaval060/ubuntu2204_python_ollama_llama3_x86

WORKDIR /app

COPY .. /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY ./project_script.sh /project_script.sh
RUN chmod +x /project_script.sh

CMD ["/project_script.sh"]