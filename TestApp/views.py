from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProdutoForm
from .models import Produto
import requests


def criarMenu(request):

    url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produtos/FSADQ5LBJLYGTSM'
    headers = {}
    response = requests.request('GET', url, headers=headers, allow_redirects=False)
    produtos = []

    if response.status_code == 200:
        for raw in response.json()['produtos']:
            raw['DESCRICAO'] = '' if raw['DESCRICAO'] is None else raw['DESCRICAO']
            produto = Produto.objects.create(**{'codigo': int(raw['CODIGO']),
                                                'nome': raw['NOME'],
                                                'descricao': raw['DESCRICAO'],
                                                'preco': float(raw['PRECO']),
                                                'tipo': raw['TIPO'],
                                                })
            produtos.append(produto)
        return render(request, 'base.html', {'produtos': produtos})
    else:
        msg = 'Ocorreu um erro ao tentar se comunicar com a API:\n' + response.text
        messages.info(request, msg)

    return render(request, 'base.html', {'produtos': produtos})


def adicionarProduto(request):
    form = ProdutoForm(request.POST or None)

    if form.is_valid():
        data = dict(form.cleaned_data)
        data['codigo'] = str(data['codigo'])
        data['tipo'] = data['tipo'].upper()
        data['descricao'] = '' if data['descricao'] is None else data['descricao']

        error = False

        # testar o tipo do produto e valido
        if data['tipo'] not in ('A', 'B', 'S', 'E'):
            messages.info(request, 'Tipo de Produto Invalido')
            error = True

        if not error:
            # testar se codigo fornercido e unico produto
            url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produtos/FSADQ5LBJLYGTSM'
            headers = {}
            response = requests.request('GET', url, headers=headers, allow_redirects=False)

            for produto in response.json()['produtos']:
                if data['codigo'] == produto['CODIGO']:
                    messages.info(request, 'Codigo de produto ja existente em nossa database')
                    error = True
                    break

        if not error:
            # enviar requisicao para adicionar produto
            url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produto/add'
            payload = "{ \n\t\"token\":   \""+'FSADQ5LBJLYGTSM'+ \
                        "\",\n\t\"codigo\": \""+str(data['codigo'])+ \
                          "\",\n\t\"nome\":   \""+data['nome']+ \
                          "\",\n\t\"preco\":  "+str(data['preco'])+ \
                          ",\n\t\"tipo\": \""+data['tipo']+ \
                          "\",\n\t\"descricao\": \""+data['descricao']+ \
                          "\"\n}"
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)

            if response.status_code == 200: # OK
                messages.info(request, 'Produto com  Codigo ' + str(data['codigo']) + '  adicionado com sucesso', extra_tags='sucesso')
                return redirect('criarMenu') # voltar tela inicial
            else:
                messages.info(request, 'Erro interno na API\n' + response.text)

    return render(request, 'produto-form.html', {'form': form, 'title': 'Novo Produto'})


def atualizarProduto(request, id):

    url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produtos/FSADQ5LBJLYGTSM'
    headers = {}
    response = requests.request('GET', url, headers=headers, allow_redirects=False)
    produto = None
    for i in response.json()['produtos']:
        if int(i['CODIGO']) == id:
            produto = Produto.objects.create(**{'codigo': int(i['CODIGO']),
                                                'nome': i['NOME'],
                                                'descricao': i['DESCRICAO'],
                                                'preco': float(i['PRECO']),
                                                'tipo': i['TIPO'],
                                                })
            break
    form = ProdutoForm(request.POST or None, instance=produto)
    form.codigo = id

    if form.is_valid():

        data = dict(form.cleaned_data)
        data['descricao'] = '' if data['descricao'] is None else data['descricao']
        data['tipo'] = data['tipo'].upper()

        error = False

        # testar o tipo do produto e valido
        if data['tipo'] not in ('A', 'B', 'S', 'E'):
            messages.info(request, 'Tipo de produto invalido')
            error = True

        if not error:
            # enviar requisicao para atualizar o arquivo
            url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produto/' + str(produto.codigo) + '/update'

            payload = "{\n\t\"token\":   \""+'FSADQ5LBJLYGTSM'+ \
                              "\",\n\t\"nome\":   \""+data['nome']+ \
                              "\",\n\t\"preco\":  "+str(data['preco'])+ \
                              ",\n\t\"tipo\": \""+data['tipo']+ \
                              "\",\n\t\"descricao\": \""+data['descricao']+ \
                              "\"\n}"
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)

            if response.status_code == 200: # OK
                messages.info(request, 'Produto com Codigo ' + str(produto.codigo) + ' alterado com sucesso ', extra_tags='sucesso')
                return redirect('criarMenu')  # voltar tela inicial
            else:
                messages.info(request, 'Erro interno na API\n' + response.text)

    return render(request, 'produto-form.html', {'form': form, 'title': 'Alterar Produto Codigo ' + str(id)})


def deletarProduto(request, id):

    url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produtos/FSADQ5LBJLYGTSM'
    headers = {}
    response = requests.request('GET', url, headers=headers, allow_redirects=False)
    produto = None

    for i in response.json()['produtos']:
        if int(i['CODIGO']) == id:
            produto = Produto.objects.create(**{'codigo': int(i['CODIGO']),
                                                'nome': i['NOME'],
                                                'descricao': i['DESCRICAO'],
                                                'preco': float(i['PRECO']),
                                                'tipo': i['TIPO'],
                                                })
            break

    if request.method == 'POST':

        # enviar requisicao oara deletar o id (codigo)
        url = 'http://briansilva1.zeedhi.com/workfolder/processoseletivo/sistemaprodutos/produto/' + str(produto.codigo) +'/delete'
        payload = "{\n\t\"token\": \"FSADQ5LBJLYGTSM\"\n}"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200: # OK
            messages.info(request, 'Produto com Codigo' + str(produto.codigo) + ' removido sucesso', extra_tags='sucesso')
        else:
            messages.info(request, 'Erro interno na API\n' + response.text)

        return redirect('criarMenu')

    return render(request, 'confirm-remove.html', {'produto': produto}) # mudar de pagina