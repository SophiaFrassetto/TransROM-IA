import logging


def setup_logging():
    """
    Configura o logging global do projeto.
    Loga para o console com formato customizado e nível INFO.
    Pronto para extensão para logs em arquivo, rotação, etc.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Exemplo de extensão para log em arquivo:
    # file_handler = logging.FileHandler('output.log')
    # file_handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(formatter)
    # logging.getLogger().addHandler(file_handler)
