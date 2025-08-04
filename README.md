# Desafio-da-Historia-premidada

## Historia
 
Criar backend que dado um objeto ele consulte uma api externa para completar os dados do correntista.
 
 
### Descrição
 
**COMO UM** novo correntista
**QUERO** passar o CEP
**PARA QUE** eu possa fazer meu cadastro
 
### Critério de Aceitação
 
* Código fonte deve esta salvo no github.
* Funcionar em container.
* Funcionar no formato openAPI.
* Ter swagger para acessar as funcoes.
* Ter log INFO falando das consultas.
* Ter log ERROR para Ceps invalidos.
* Ter log CRITICAL quando não tiver acesso a api.
* Deve ter uma esteira onde ao versionar (tag) no codigo ele disponibilize uma imagem no docker hub.
* Rodar na maquina local baixando a imagem no docker hub.(docker.binarios.bb.com.br/user-docker/imagem:versao)
* Consulta o CEP na api externa https://brasilapi.com.br/docs#tag/CEP
 
 
### Cenário de teste
 
**DADO QUE** mande o objeto *cliente* por metodo GET
**QUANDO** receber a requisição com cep valido.
**ENTÃO** devolver o objeto *clienteEndereço*
 
**DADO QUE** mande o objeto *cliente* por metodo GET
**QUANDO** receber a requisição com cep invalido.
**ENTÃO** devolver o erro de cep invalido, e logar como ERROR
 
Objetos:

*cliente*
```json
{
    "cpf": "string (required)",
    "nome": "string (required)",
    "cep": "integer <int64> (required)"
}
```
*clienteEndereço*
```json
{
    "cpf": "string (required)",    
    "cep": "integer <int64> (required)",
    "state": "string",
    "city": "string",
    "neighborhood": "string",
    "street": "string",
    "service": "viacep"
}
```

Para rodar, execute os comandos abaixo no terminal dentro da pasta do projeto:
```shell
docker build -t fastapi-cep-app .
docker run -p 8000:8000 fastapi-cep-app
```
Agora, basta acessar o endereço http://localhost:8000/docs no navegador para testar a api através do swagger ui.

# Como executar a sua aplicação
## Docker
O Docker serve para criar um ambiente para nosso aplicativo, com o básico para executá-lo

### Como "buildar" e executar a sua aplicação:
```
   docker build -t app/desafio-genuv:1.0 .
```
Esse comando vai construir sua imagem baseado no dockerfile na raíz do seu projeto. Utilize a versão de acordo com a tag do código

```
   docker run -p 8000:8000 [opcional: -e http://ip:porta] --name desafio-genuv app/desafio-genuv:1.0
```
Esse comando vai executar sua imagem docker. A inserção do proxy é opcional. Como o projeto utiliza de uma API externa, as vezes é bloqueado pelo proxy.

Agora, basta acessar o endereço http://localhost:8000/docs no navegador para testar a api através do swagger ui.
 
### Local:
Na raiz do seu projeto, vamos habilitar a permissão de execução do nosso bash
```
   chmod +x ./run.sh
```
Esse comando habilita a permissão de execução do bash

```  
  ./run.sh
```
Esse comando executa o bash, que executa o projeto. Esse bash é utilizado para executar o aplicativo localmente, caso desejado. Ele irá verificar se, na raiz do projeto, há um *.env* (arquivo de variável de ambiente) e uma pasta *venv* (pasta de ambiente virtual).

Agora, basta acessar o endereço http://localhost:8001/docs no navegador para testar a api através do swagger ui.

**OBSERVAÇÃO:** foi feito uma alteração nas portas de acordo com o tipo de execução: 
```
Docker: porta 8000 
Local: porta 8001
```
Isso permite que você rode, tanto localmente, quando conteinerizado, o seu aplicativo.
