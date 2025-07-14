# 定义虚拟环境目录变量
VENV_DIR = venv

# 'init' 目标：初始化虚拟环境并安装依赖包
init: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

# 'run' 目标：运行主程序
run: $(VENV_DIR)/bin/activate
	./start.sh\

# 'clean' 目标：删除虚拟环境
clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment cleaned."

# 如果虚拟环境目录不存在，则创建虚拟环境
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created. Run 'make init' to install dependencies."


# make init  # 初始化虚拟环境并安装依赖
# make run   # 运行项目
# make clean # 清理虚拟环境
