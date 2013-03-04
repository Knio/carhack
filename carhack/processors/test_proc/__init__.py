
from carhack import app
from carhack.processors import Processor, subscribe

class TestProcessor(Processor):
  def __init__(self, pub):
    super(TestProcessor, self).__init__(pub)
    self.value = 0.0

  @subscribe('test_sensor.sin1')
  def cos1(self, ts, value):
    self.value += value
    self.publish('cos1', self.value)

processor = TestProcessor
