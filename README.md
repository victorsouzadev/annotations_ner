
# Ferramenta de Anotação de NER

Esta é uma ferramenta simples de anotação de entidades nomeadas (NER) utilizando o **Tkinter** para a interface gráfica e **spaCy** para a estrutura de processamento de linguagem natural. Ela permite que o usuário selecione textos e os anote como entidades personalizadas, salvando as anotações em arquivos `.json` incrementais.

## Funcionalidades

- Anotação de textos com entidades nomeadas.
- Gerenciamento de tipos de entidades personalizados.
- Salvar anotações em arquivos JSON para uso futuro.
- Interface gráfica amigável para a seleção de entidades e gerenciamento de anotações.

## Requisitos

Certifique-se de ter as seguintes dependências instaladas:

- Python 3.x
- Tkinter (geralmente já vem instalado com o Python)
- SpaCy

Instale as dependências executando o comando abaixo:

```bash
pip install spacy
```

## Configuração

Antes de começar, você pode configurar um modelo em português do spaCy, executando:

```bash
python -m spacy download pt_core_news_sm
```

**Nota**: A aplicação está configurada para utilizar um modelo vazio de spaCy (`spacy.blank("pt")`). Caso deseje usar um modelo pré-treinado, substitua `spacy.blank("pt")` por `spacy.load("pt_core_news_sm")` no código.

## Como Usar

1. **Executar a aplicação**: Para iniciar a ferramenta de anotação, basta executar o arquivo Python principal.

```bash
python nome_do_arquivo.py
```

2. **Anotar Entidades**:
   - Selecione um trecho de texto no campo principal da interface.
   - Clique em **Anotar Entidade**. Uma janela será exibida para você escolher ou adicionar o tipo de entidade correspondente ao trecho selecionado.
   - As entidades anotadas serão destacadas no texto com um fundo amarelo.

3. **Salvar Anotações**:
   - Após realizar anotações, clique em **Salvar Anotações**. Isso irá salvar o texto anotado em um arquivo `annotations_XX.json`, onde `XX` será o número incremental, evitando a sobreposição de arquivos.
   - O texto e as anotações serão limpos após o salvamento.

4. **Gerenciar Entidades**:
   - Você pode adicionar novas entidades clicando no botão **Gerenciar Entidades**. Isso abrirá uma janela para você adicionar uma nova entidade ao conjunto existente.

5. **Arquivos**:
   - As anotações serão salvas como arquivos JSON no formato:
     ```json
     {
       "text": "Texto anotado",
       "entities": [
         [inicio, fim, "tipo_de_entidade"]
       ]
     }
     ```
   - As entidades são armazenadas no arquivo `entities.json`, que pode ser editado ou gerenciado pela interface.

## Estrutura do Projeto

- **annotations_XX.json**: Arquivos JSON incrementais contendo as anotações de texto.
- **entities.json**: Arquivo JSON que armazena os tipos de entidades gerenciados.
- **anotation.py**: Arquivo Python principal que contém o código da ferramenta.

## Exemplo de Uso

Ao iniciar a aplicação, um editor de texto será exibido. Você pode digitar ou colar o texto que deseja anotar. Selecione partes do texto e escolha a entidade correspondente. As anotações serão salvas em arquivos incrementais.

## Licença

Este projeto está sob a licença MIT.
