from django.contrib import admin

# https://medium.com/@hakibenita/how-to-turn-django-admin-into-a-lightweight-dashboard-a0e0bbf609ad

from .models import time_summary, time_entry
from django.db.models import Count, Sum, Min, Max, DateTimeField
from django.db.models.functions import Trunc

class TimeEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')

admin.site.register(time_entry, TimeEntryAdmin)

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'

@admin.register(time_summary)
class time_summaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'
    date_hierarchy = 'created_at'
    
    actions = None
    # Prevent additional queries for pagination.
    show_full_result_count = False

    list_filter = (
        'name',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        # self.get_queryset would return the base queryset. ChangeList
        # apply the filters from the request so this is the only way to
        # get the filtered queryset.

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            # See issue #172.
            # When an invalid filter is used django will redirect. In this
            # case the response is an http redirect response and so it has
            # no context_data.
            return response


        # List view
        #print(qs)

        metrics = {
            'total': Count('id'),
            'total_sales': Sum('hours_worked'),
        }

        response.context_data['summary'] = list(
            qs
            .values('name')
            .annotate(**metrics)
            .order_by('-total_sales')
        )
        print("summary:",response.context_data['summary'])

        # List view summary

        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))
        print("summary_total", response.context_data['summary_total'])

        # Chart

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        
        print("period:",period)
        
        response.context_data['period'] = period
        
        summary_over_time = qs.annotate(
            period=Trunc(
                'created_at',
                period,
                output_field=DateTimeField(),
            ),
        ).values('period').annotate(total=Sum('hours_worked')).order_by('period')
        
        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
               ((x['total'] or 0) - low) / (high - low) * 100
               if high > low else 0,
            
        } for x in summary_over_time]
        
        print("summary over time",response.context_data['summary_over_time'] )

        return response
    
    