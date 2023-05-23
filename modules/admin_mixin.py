class AdminMediaMixin:
    class Media:
        extend = True
        css = {
            'all': (
                'admin/css/buttons.css',
                'admin/css/admin_custom.css',
            )
        }
        js = ('admin/js/custom_admin.js',)
