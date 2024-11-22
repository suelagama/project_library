import json

from django.views.generic import TemplateView

from library.models import DashboardManager


class DashboardView(TemplateView):
    template_name = 'dashboard/pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard = DashboardManager()
        monthly_statistics = list(DashboardManager.get_monthly_statistics())
        day_statistics = list(DashboardManager.get_day_statistics())

        context['general_statistics'] = dashboard.get_general_statistics()
        context['popular_books'] = dashboard.get_most_borrowed_books()
        context['monthly_statistics'] = json.dumps(
            monthly_statistics, default=str)

        context['day_statistics'] = json.dumps(
            day_statistics, default=str)

        context['page_title'] = 'Dashboard'
        return context
