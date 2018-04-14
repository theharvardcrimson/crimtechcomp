import datetime
import logging

from django.conf import settings

from adspygoogle.common.Client import _GOOGLE_OAUTH2_ENDPOINT
from adspygoogle.dfp.DfpClient import DfpClient
from oauth2client.client import OAuth2Credentials

from .models import AdUnit

__all__ = ['DoubleClickNetwork', 'BaseNetwork']
logger = logging.getLogger(__name__)


class BaseNetwork(object):
    def update_ad_units(self):
        try:
            return self._update_ad_units()
        except Exception as e:
            message = 'Fetching ad units from network failed: %s' % e
            logger.exception(message)
            raise StandardError(message)

    def _update_ad_units(self):
        raise NotImplementedError


class DoubleClickNetwork(BaseNetwork):
    VERSION = 'v201306'
    AD_UNIT_PREFIX = 'TheCrimson'
    MOBILE_KEY = 'Mobile'
    DESKTOP_KEY = 'Desktop'

    def __init__(self):
        auth = dict(settings.DFP_HEADERS)
        auth['oauth2credentials'] = OAuth2Credentials(
            None, auth['clientId'], auth['clientSecret'], auth['refreshToken'],
            datetime.datetime(1980, 1, 1, 12), _GOOGLE_OAUTH2_ENDPOINT,
            'Google Ads* Python Client Library')
        self.client = DfpClient(
            headers=auth,
            config=settings.DFP_CONFIG)

    def get_root_node_id(self):
        network_service = self.client.GetNetworkService(version=self.VERSION)
        network = network_service.GetCurrentNetwork()[0]
        return network['effectiveRootAdUnitId']

    def _update_ad_units(self):
        inventory = self.client.GetInventoryService(version=self.VERSION)
        values = [{
            'key': 'parentId',
            'value': {
                'xsi_type': 'TextValue',
                'value': self.get_root_node_id()
            }
        }]
        filter_statement = {
            'query': "WHERE status = 'ACTIVE' AND parentId = :parentId",
            'values': values
        }
        ad_units = inventory.GetAdUnitsByStatement(filter_statement)[0]
        ad_units = ad_units.get('results', [])
        for ad_unit in ad_units:
            if not ad_unit['adUnitCode'].startswith(self.AD_UNIT_PREFIX):
                continue

            AdUnit.objects.create_or_update(
                code=ad_unit['adUnitCode'],
                network_id=ad_unit['id'],
                size=ad_unit['adUnitSizes'][0]['fullDisplayString'],
                display_on=AdUnit.MOBILE_AND_DESKTOP)


ad_network = DoubleClickNetwork()
