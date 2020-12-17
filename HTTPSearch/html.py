def make_html_table(body, data, cols):
    body.append('<table>')
    body.append('<thead><tr>')
    add_table_cells(body,
                    list(map(lambda col: col['label'], cols)),
                    list(map(lambda col: {'label': col['label'], 'show': col.get('show', True)}, cols)),
                    'th')
    body.append('</tr></thead>')

    body.append('<tbody>')
    for row in data:
        body.append('<tr>')
        add_table_cells(body, row, cols)
        body.append('</tr>')
    body.append('</tbody>')
    body.append('</table>')

    return body


def add_table_cells(body, row, cols, cell_type='td'):
    idx = -1
    col_skip = 0
    for col in cols:
        if col_skip > 0:
            col_skip -= 1
            continue
        idx += 1
        attrs = ''
        cell_settings = None
        cls = col.get('class', None)
        show = col.get('show', True)
        prefix = col.get('prefix', '')
        suffix = col.get('suffix', '')
        span_col = col.get('span_count', None)
        span_idx = col.get('span_index', None)
        value_lambda = col.get('value', None)

        if span_col and span_idx and len(row) > span_idx:
            if row[span_idx] == 1:
                attrs += ' rowspan="%i"' % row[span_col]
            else:
                continue

        if not show:
            continue

        if len(row) > idx:
            val = row[idx]
        else:
            val = None

        if isinstance(val, dict):
            cell_settings = val
            val = cell_settings.get('value', None)

        if callable(value_lambda):
            try:
                val = value_lambda(val)
            except:
                pass
        elif value_lambda and not val:
            val = value_lambda

        if callable(cls):
            try:
                cls = cls(val)
            except:
                pass

        if cell_settings:
            # Override column settings
            if 'colspan' in cell_settings:
                attrs += ' colspan="%i"' % int(cell_settings['colspan'])
                col_skip = int(cell_settings['colspan']) - 1
            if 'class' in cell_settings:
                cls = cell_settings['class']

        if cls: attrs += ' class="' + cls + '"'

        if val.endswith('.jpg'):
            cell = u'<%s><a href = %s > %s </a></%s>' % (cell_type, val, row[0], cell_type)
        elif val.startswith('https://') and not val.endswith('.jpg'):
            cell = u'<%s><a href = %s > %s </a></%s>' % (cell_type, val, row[0], cell_type)
        else:
            cell = u'<%s%s>%s%s%s</%s>' % (cell_type, attrs, prefix, val or '&nbsp;',
                                           suffix, cell_type)
        body.append(cell)
