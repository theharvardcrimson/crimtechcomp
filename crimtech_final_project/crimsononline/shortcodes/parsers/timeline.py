from django.template.loader import render_to_string


def parse(kwargs):
    data = {}
    nEvents = int(kwargs.get('num'))
    data['n'] = nEvents
    data['events'] = []

    for i in range(1, nEvents + 1):
        eTime = kwargs.get('time' + str(i), ' ')
        eDate = kwargs.get('date' + str(i), ' ')
        eEvent = kwargs.get('event' + str(i), ' ')
        data['events'].append([eTime, eDate, eEvent])

    return render_to_string('shortcodes/timeline.html', data)
