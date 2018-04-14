def ret_on_fail(fn, retval, exception_tuple=Exception):
    """Function modifier to return retval if an exception is thrown.

    Does not work well as a decorator, cause I'm not that 1337.

    Only gives retval if the exception is in exception_tuple,
    otherwise, reraises the exception.
    """
    def fn_prime(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except exception_tuple:
            return retval
        except:
            raise
    return fn_prime


def to_child(qs, n, ctype=None):
    if ctype is not None:
        ans = []
        max_len = qs.count()
        i = 0
        while len(ans) < n and i < max_len:
            if qs[i].content_type.model == ctype:
                ans.append(qs[i].child)
            i += 1
        return ans
    else:
        return [c.child for c in qs[:n]]
