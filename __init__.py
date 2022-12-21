from trytond.pool import Pool

__all__ = ['register']


def register():
    Pool.register(
        module='zebra_print', type_='model')
    Pool.register(
        module='zebra_print', type_='wizard')
    Pool.register(
        module='zebra_print', type_='report')
