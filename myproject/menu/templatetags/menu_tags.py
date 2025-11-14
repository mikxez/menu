from django import template
from menu.models import MenuItem
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    items = list(
        MenuItem.objects.filter(menu__name=menu_name)
            .select_related('parent', 'menu')
            .order_by('id')
    )

    if not items:
        return {'menu_tree': []}

    resolved_url = {}
    for item in items:
        if not item.url:
            resolved_url[item.id] = ''
            continue

        try:
            resolved_url[item.id] = reverse(item.url)
        except NoReverseMatch:
            resolved_url[item.id] = item.url

    children_map = {}
    for item in items:
        parent_id = item.parent_id if item.parent_id else None
        children_map.setdefault(parent_id, []).append(item)

    active_item = None
    for item in items:
        if resolved_url[item.id] == current_path:
            active_item = item
            break

    active_branch = set()
    if active_item:
        cur = active_item
        while cur:
            active_branch.add(cur.id)
            cur = cur.parent

    def build_tree(parent_id=None):
        result = []
        children = children_map.get(parent_id, [])

        for item in children:
            child_nodes = build_tree(item.id)
            is_active = item.id in active_branch
            is_open = is_active or any(c.get('is_open') for c in child_nodes)

            if is_active:
                for c in child_nodes:
                    c['is_open'] = True

            result.append({
                'item': item,
                'children': child_nodes,
                'is_active': is_active,
                'is_open': is_open,
                'resolved_url': resolved_url[item.id]
            })

        return result

    menu_tree = build_tree()

    return {'menu_tree': menu_tree}
