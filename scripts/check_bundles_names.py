import sys
sys.path.append('E:/Airtel/prototype')
import recommendation_engine as re_eng

print([x for x in dir(re_eng) if not x.startswith('__')])
