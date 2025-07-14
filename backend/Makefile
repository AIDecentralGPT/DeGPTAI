<<<<<<< HEAD
# Define virtual environment directory variables
VENV_DIR = venv

# 'init' Goal: Initialize the virtual environment and install dependency packages
=======
# 定义虚拟环境目录变量
VENV_DIR = venv

# 'init' 目标：初始化虚拟环境并安装依赖包
>>>>>>> fingerprintAuth-out
init: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

<<<<<<< HEAD
# 'run' Goal: Run the main program
run: $(VENV_DIR)/bin/activate
	./start.sh\

# 'clean' Goal: Delete virtual environment
=======
# 'run' 目标：运行主程序
run: $(VENV_DIR)/bin/activate
	./start.sh\

# 'clean' 目标：删除虚拟环境
>>>>>>> fingerprintAuth-out
clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment cleaned."

<<<<<<< HEAD
# If the virtual environment directory does not exist, create a virtual environment
=======
# 如果虚拟环境目录不存在，则创建虚拟环境
>>>>>>> fingerprintAuth-out
$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created. Run 'make init' to install dependencies."


<<<<<<< HEAD
# make init  # Initialize virtual environment and install dependencies
# make run   # Run Project
# make clean # Clean up virtual environment
=======
# make init  # 初始化虚拟环境并安装依赖
# make run   # 运行项目
# make clean # 清理虚拟环境
>>>>>>> fingerprintAuth-out
