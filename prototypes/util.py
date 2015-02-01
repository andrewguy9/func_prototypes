"""
For each key in d1, return a dict which has {key:(d1[key],d2[key])}.
Raises KeyError if d2 does not contain a key
"""
def dictjoin(d1, d2):
  out = {}
  for (k, d1v) in d1.items():
    try:
      d2v = d2[k]
    except KeyError as e:
      raise e
    else:
      out[k] = (d1v, d2v)
  return out

