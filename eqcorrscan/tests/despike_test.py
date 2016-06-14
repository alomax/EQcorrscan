"""Test the despiking algorithms implimented in EQcorrscan."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest


class DespikeTesting(unittest.TestCase):
    def test_median_filter(self):
        """Test the median filter implimentation."""
        import numpy as np
        from obspy.core import Trace
        from eqcorrscan.utils.despike import median_filter
        spiked = np.random.randn(1000)
        # Put some spikes in there
        spiked[100] = 20
        spiked[400] = 40
        spiked[450] = -40
        spiked = Trace(spiked)
        spiked.stats.sampling_rate = 100
        despiked = median_filter(tr=spiked, multiplier=10,
                                 windowlength=0.5, interp_len=0.05)
        self.assertNotEqual(despiked.data[100], 20)
        self.assertNotEqual(despiked.data[400], 40)
        self.assertNotEqual(despiked.data[450], -40)

    def test_template_remove(self):
        """Test the despiker based on correlations."""
        import numpy as np
        from obspy.core import Trace
        from eqcorrscan.utils.despike import template_remove
        spiked = np.random.randn(1000)
        # Put some spikes in there
        spiked[100] = 20
        spiked[400] = 40
        spiked[450] = -40
        spiked = Trace(spiked)
        spiked.stats.sampling_rate = 100
        template = np.zeros(10)
        template[2] = 1
        template = Trace(template)
        template.stats.sampling_rate = 100
        despiked = template_remove(tr=spiked, template=template, cc_thresh=0.3,
                                   windowlength=0.5, interp_len=0.05, debug=0)
        self.assertNotEqual(despiked.data[100], 20)
        self.assertNotEqual(despiked.data[400], 40)
        self.assertEqual(despiked.data[450], -40)


if __name__ == '__main__':
    """
    Run core tests
    """
    unittest.main()