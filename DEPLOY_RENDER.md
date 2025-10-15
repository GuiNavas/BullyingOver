# 🚀 Deploy no Render - Instruções Completas

## 📋 **Pré-requisitos**
- Conta no GitHub
- Conta no Render (gratuita)
- Projeto organizado na pasta `bullying-main`

## 🔧 **Passo a Passo**

### **1. Upload para GitHub**
1. **Crie um repositório** no GitHub
2. **Faça upload** da pasta `bullying-main` completa
3. **Certifique-se** de que todos os arquivos estão na raiz do repositório

### **2. Configuração no Render**
1. **Acesse**: [render.com](https://render.com)
2. **Faça login** com sua conta GitHub
3. **Clique em**: "New +" → "Web Service"
4. **Conecte** seu repositório GitHub
5. **Selecione** o repositório do projeto

### **3. Configurações do Serviço**
```
Name: bullying-site (ou nome de sua escolha)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free (ou Starter para melhor performance)
```

### **4. Deploy Automático**
- O Render detectará automaticamente o Flask
- O build será executado automaticamente
- Você receberá uma URL pública (ex: `https://bullying-site.onrender.com`)

## 📁 **Arquivos Necessários**

### ✅ **Arquivos Principais**
- `app.py` - Aplicação Flask
- `requirements.txt` - Dependências
- `Procfile` - Configuração de deploy
- `README.md` - Documentação

### ✅ **Arquivos Estáticos**
- `static/css/style.css` - Estilos customizados
- `static/css/bootstrap.min.css` - Bootstrap
- `static/js/script.js` - JavaScript
- `static/js/bootstrap.bundle.min.js` - Bootstrap JS
- `static/img/logo.png` - Logo do site

### ✅ **Templates**
- `templates/base.html` - Template base
- `templates/index.html` - Página inicial
- `templates/sobre.html` - Página sobre
- `templates/estatisticas.html` - Estatísticas
- `templates/denuncia.html` - Formulário de denúncia
- `templates/contato.html` - Formulário de contato

## 🔍 **Verificações Importantes**

### **Antes do Deploy**
- [ ] Todos os arquivos estão na pasta raiz
- [ ] `requirements.txt` contém todas as dependências
- [ ] `Procfile` está configurado corretamente
- [ ] `.gitignore` está presente
- [ ] `README.md` está atualizado

### **Após o Deploy**
- [ ] Site carrega corretamente
- [ ] Todas as páginas funcionam
- [ ] Formulários estão funcionando
- [ ] Responsividade mobile está OK
- [ ] Gráficos de estatísticas aparecem

## 🐛 **Solução de Problemas**

### **Erro de Build**
- Verifique se todas as dependências estão no `requirements.txt`
- Confirme se o `Procfile` está correto
- Verifique se não há arquivos desnecessários

### **Erro 500**
- Verifique os logs no Render
- Confirme se o banco de dados está sendo criado
- Verifique se todas as rotas estão funcionando

### **Site não carrega**
- Verifique se a URL está correta
- Confirme se o serviço está rodando
- Verifique se não há erros de sintaxe

## 📱 **Teste Pós-Deploy**

### **Desktop**
- Acesse a URL fornecida pelo Render
- Teste todas as páginas
- Verifique formulários

### **Mobile**
- Acesse pelo celular
- Teste responsividade
- Verifique formulários mobile

## 🎯 **URLs de Teste**
- **Início**: `https://seu-app.onrender.com/`
- **Sobre**: `https://seu-app.onrender.com/sobre`
- **Estatísticas**: `https://seu-app.onrender.com/estatisticas`
- **Denúncia**: `https://seu-app.onrender.com/denuncia`
- **Contato**: `https://seu-app.onrender.com/contato`

## ⚡ **Dicas de Performance**

### **Render Free**
- Pode ter "cold start" (demora para carregar)
- Ideal para testes e projetos pequenos
- Limite de horas de uso

### **Render Starter**
- Melhor performance
- Sem "cold start"
- Ideal para produção

## 🔄 **Atualizações**

### **Para atualizar o site**
1. Faça as alterações localmente
2. Faça commit e push para o GitHub
3. O Render fará deploy automático
4. Aguarde alguns minutos para o build

---

**🎉 Seu site estará online em poucos minutos!**
