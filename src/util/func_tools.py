import argparse


class FuncTools:
    @staticmethod
    def run_as_admin(function):
        # 构造 以管理员运行的输入参数
        def wrapper():
            parser = argparse.ArgumentParser()
            parser.add_argument('--run-as-admin', action='store_true')
            args = parser.parse_args()
            function()
        return wrapper
