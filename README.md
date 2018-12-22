# ifcrush
Rede Social para troca de mensagens para fomentar a educação inclusiva durante a Semana Nacional de Ciência e Tecnologia do Instituto Federal do Amapá - 2018

O foco era que houvesse interação entre alunos, no caso, para que se declarassem para seus crushs sem medo de ser identificado ou correr o risco de ser rejeitado, possibilitando assim interação em anonimato. Contudo, todas as mensagens são filtradas no painel administrativo com o objetivo de evitar excessos ou ataques devido ao anonimato. 

# Informações para Teste

Para facilitar os testes, você pode apontar o `pip` para o arquivo `requirements.txt` e instalar as dependências do projeto:

```
# pip install -r requirements.txt
```

Após isso, crie um banco de dados em um SGBD de sua preferência e acesse o arquivo `settings.py` e altere as linhas 80 à 89:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ifcrush',
        'USER': 'root',
        'PASSWORD': 'toor',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

Para testar se a conexão com o banco está funcionando corretamente, basta tentar aplicar uma migração na pasta do projeto:

```
$ python manage.py migrate
```

Depois criar um superusuário:

```
$ python manage.py createsuperuser 
```

Adiciona as informações, e quando tudo estiver ok:

```
$ python manage.py runserver
```

O Django irá rodar o servidor embutido no projeto e rodará no localhost de sua máquina, se tudo estiver ok, é só acessar a aplicação. =)

# Licença

GPL
