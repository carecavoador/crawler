- Corrigir bug de pasta do dia não localizada:
    Traceback (most recent call last):
    File "E:\python\crawler\crawler.py", line 208, in <module>
        main()
    File "E:\python\crawler\crawler.py", line 186, in main
        work(jobs_to_do, LAYOUTS_FOLDER, PROOFS_FOLDER, OUTPUT_FOLDER)
    File "E:\python\crawler\crawler.py", line 125, in work
        layouts_done = retreive_job_files(
    File "E:\python\crawler\crawler.py", line 87, in retreive_job_files
        found_files = find_job_files(job, location)
    File "E:\python\crawler\crawler.py", line 62, in find_job_files
        files = os.listdir(location)
    FileNotFoundError: [WinError 3] O sistema não pode encontrar o caminho especificado: 'F:\\blumenau\\Print Layout\\21-06-2022'
- Identificar se o arquivo de origem está zipado e descompactar no destino.
- Determinar o tamanho do arquivo de print e salvar em PDF dentro da pasta correspondente ao respectivo tamanho.
- Buscar por arquivos de OS manualmente via CLI (opções -L -P --job)
- Corrigir o logger.
- Criar um banco de dados para os dados dos Jobs executados.