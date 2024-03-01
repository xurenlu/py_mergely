from zeroconf import Zeroconf, ServiceInfo
import socket

def main():
    # 初始化 Zeroconf 实例
    zeroconf = Zeroconf()

    # 准备服务注册信息
    service_type = "_http._tcp.local."
    service_name = "web1._http._tcp.local."
    service_port = 80
    server_name = socket.gethostname() + ".local."

    # 获取本地 IP 地址
    local_ip_address = socket.inet_aton(socket.gethostbyname(socket.gethostname()))

    # 创建 ServiceInfo 对象
    service_info = ServiceInfo(
        service_type,
        service_name,
        addresses=[local_ip_address],
        port=service_port,
        server=server_name,
        properties={},
    )

    # 注册服务
    print(f"Registering service {service_name}, type {service_type}, port {service_port}")
    zeroconf.register_service(service_info)

    # 等待用户中断 (Ctrl-C)
    try:
        input("Service registered. Press Enter to exit...\n\n")
    finally:
        # 注销服务并关闭 Zeroconf
        zeroconf.unregister_service(service_info)
        zeroconf.close()
        print("Service unregistered.")

if __name__ == "__main__":
    main()
