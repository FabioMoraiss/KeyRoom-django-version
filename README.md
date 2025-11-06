# KeyRoom: O cofre da sua vida online

Bem-vindo ao **KeyRoom**, seu cofre digital feito para proteger e organizar suas credenciais e senhas de forma prática e segura!  
Este repositório traz um protótipo do KeyRoom desenvolvido em Django, baseado nos conhecimentos adquiridos na disciplina de Projeto Web 2 no IFPR.

---

## 🚀 Como rodar o projeto

Siga os passos abaixo para rodar localmente:

```bash
git clone https://github.com/FabioMoraiss/KeyRoom-django-version.git
cd KeyRoom-django-version/keyRoom
pip install -r requirements.txt
python manage.py runserver 8080
```

Acesse [http://localhost:8080](http://localhost:8080) para usar o site!

---

## ✨ Funcionalidades principais

- **Gestão de credenciais:** armazene e categorize suas credenciais.
- **Gerador de senhas:** cria passwords fortes direto do navegador.
- **Compartilhamento seguro:** compartilhe credenciais com usuários confiáveis.
- **Gestão de usuários confiáveis:** controle quem pode acessar informações compartilhadas.
- **Gerenciamento de tags:** personalize e organize suas credenciais por categorias.

---

## 🗃️ Entidades

O sistema possui alguns dos principais models abaixo (resumidos):

- `CustomUser`: Extensão do usuário padrão do Django, com campo de código único.
- `CustomTag`: Categorias personalizadas de credenciais, vinculadas ao usuário.
- `Credential`: Onde são salvas as credenciais (título, nome de usuário, senha, URL, OTP, notas).
- `ListOfTrustedUsers`: Lista de usuários “confiáveis” para cada usuário do sistema.
- `SharedCredential`: Relação de compartilhamento de credenciais entre usuários.

---

## 🌐 Principais rotas/URLs

O KeyRoom possui endpoints para:

- **Autenticação:** login, cadastro e logout.
- **Credenciais:** listar, adicionar, editar, excluir, visualizar OTP, verificação de senhas comprometidas.
- **Gerador de Senhas:** gerar e visualizar senhas fortes.
- **Tags:** criar, editar e deletar tags personalizadas.
- **Compartilhamentos:** visualizar e realizar compartilhamento de credenciais.
- **Usuários confiáveis:** gerenciar lista de pessoas confiáveis.



---
## ⚠️ O que faltou implementar
- Criptografar as credenciais no banco de dados.
- Testes automatizados.
---

## 📚 Créditos

Desenvolvido por Fabio Morais para a disciplina de Projeto Web 2 no IFPR - 2025.

---
<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2.13-green" alt="Django Version">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python Version">
</p>