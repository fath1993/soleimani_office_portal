def fetch_data_from_http_post(request, item, context, empty_none: bool = None):
    try:
        result_item = request.POST[f'{item}']
        if empty_none:
            if result_item == '':
                result_item = None
    except:
        result_item = None
    context[f'{item}'] = result_item
    print(f'{item}: {result_item}')
    return result_item


def fetch_data_from_http_get(request, item, context):
    try:
        result_item = request.GET[f'{item}']
        if result_item == '':
            result_item = None
    except:
        result_item = None
    context[f'{item}'] = result_item
    print(f'{item}: {result_item}')
    return result_item


def fetch_files_from_http_post_data(request, item, context):
    try:
        result_item = request.FILES.getlist(f'{item}')
        if len(result_item) == 0:
            result_item = None
        else:
            for item in result_item:
                context[f'{item}'] = item
    except:
        result_item = None
    print(f'{result_item}')
    return result_item


def fetch_single_file_from_http_files(request, item, context):
    try:
        result_item = request.FILES[f'{item}']
        if result_item == '':
            result_item = None
    except:
        result_item = None
    print(f'{item}: {result_item}')
    context[f'{item}'] = result_item
    return result_item
