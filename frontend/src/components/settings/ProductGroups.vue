<template>
  <div class="product-groups">
    <!-- 组列表 -->
    <div class="group-list">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>产品组</span>
            <el-button type="primary" @click="addGroup">添加组</el-button>
          </div>
        </template>
        
        <el-table :data="groups" border>
          <el-table-column label="组名" prop="name" />
          <el-table-column label="指标" prop="target">
            <template #default="{ row }">
              <el-input-number 
                v-model="row.target" 
                :min="0"
                @change="updateGroup(row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="排序" width="100">
            <template #default="{ row, $index }">
              <el-button-group>
                <el-button 
                  :disabled="$index === 0"
                  @click="moveGroup($index, -1)"
                  icon="el-icon-top"
                  size="small"
                />
                <el-button 
                  :disabled="$index === groups.length - 1"
                  @click="moveGroup($index, 1)"
                  icon="el-icon-bottom"
                  size="small"
                />
              </el-button-group>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                size="small"
                @click="editGroup(row)"
              >
                编辑
              </el-button>
              <el-button 
                type="success" 
                size="small"
                @click="manageProducts(row)"
              >
                产品
              </el-button>
              <el-button 
                type="danger" 
                size="small"
                @click="deleteGroup(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 产品列表 -->
    <div class="product-list" v-if="selectedGroup">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>{{ selectedGroup.name }} - 产品管理</span>
            <el-button type="primary" @click="addProduct">添加产品</el-button>
          </div>
        </template>
        
        <el-table :data="products" border>
          <el-table-column label="代码" prop="code" />
          <el-table-column label="名称" prop="name" />
          <el-table-column label="最小金额" prop="min_amount">
            <template #default="{ row }">
              <el-input-number 
                v-model="row.min_amount" 
                :min="0"
                @change="updateProduct(row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button 
                type="danger" 
                size="small"
                @click="deleteProduct(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 组对话框 -->
    <el-dialog
      :title="groupDialog.title"
      v-model="groupDialog.visible"
      width="500px"
    >
      <el-form :model="groupDialog.form" label-width="80px">
        <el-form-item label="组名">
          <el-input v-model="groupDialog.form.name" />
        </el-form-item>
        <el-form-item label="指标">
          <el-input-number 
            v-model="groupDialog.form.target"
            :min="0"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="groupDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveGroup">确定</el-button>
      </template>
    </el-dialog>

    <!-- 产品对话框 -->
    <el-dialog
      title="添加产品"
      v-model="productDialog.visible"
      width="500px"
    >
      <el-form :model="productDialog.form" label-width="100px">
        <el-form-item label="产品代码">
          <el-input v-model="productDialog.form.code" />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="productDialog.form.name" />
        </el-form-item>
        <el-form-item label="最小金额">
          <el-input-number 
            v-model="productDialog.form.min_amount"
            :min="0"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="productDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProductGroups',
  data() {
    return {
      groups: [],
      products: [],
      selectedGroup: null,
      groupDialog: {
        visible: false,
        title: '',
        form: {
          name: '',
          target: 0,
          id: null
        }
      },
      productDialog: {
        visible: false,
        form: {
          code: '',
          name: '',
          min_amount: 0
        }
      }
    }
  },
  created() {
    this.fetchGroups()
  },
  methods: {
    async fetchGroups() {
      try {
        const res = await axios.get('/api/settings/product-groups')
        this.groups = res.data
      } catch (error) {
        this.$message.error('获取组列表失败')
      }
    },
    async fetchProducts() {
      if (!this.selectedGroup) return
      try {
        const res = await axios.get(`/api/settings/product-groups/${this.selectedGroup.id}/products`)
        this.products = res.data
      } catch (error) {
        this.$message.error('获取产品列表失败')
      }
    },
    addGroup() {
      this.groupDialog.title = '添加组'
      this.groupDialog.form = { name: '', target: 0, id: null }
      this.groupDialog.visible = true
    },
    editGroup(group) {
      this.groupDialog.title = '编辑组'
      this.groupDialog.form = { ...group }
      this.groupDialog.visible = true
    },
    manageProducts(group) {
      this.selectedGroup = group
      this.fetchProducts()
    },
    async saveGroup() {
      try {
        if (this.groupDialog.form.id) {
          await axios.put(`/api/settings/product-groups/${this.groupDialog.form.id}`, this.groupDialog.form)
        } else {
          await axios.post('/api/settings/product-groups', this.groupDialog.form)
        }
        this.groupDialog.visible = false
        this.fetchGroups()
        this.$message.success('保存成功')
      } catch (error) {
        this.$message.error('保存失败')
      }
    },
    async updateGroup(group) {
      try {
        await axios.put(`/api/settings/product-groups/${group.id}`, group)
        this.$message.success('更新成功')
      } catch (error) {
        this.$message.error('更新失败')
      }
    },
    async deleteGroup(group) {
      try {
        await this.$confirm('确认删除该组?', '提示', {
          type: 'warning'
        })
        await axios.delete(`/api/settings/product-groups/${group.id}`)
        this.fetchGroups()
        if (this.selectedGroup?.id === group.id) {
          this.selectedGroup = null
        }
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    },
    async moveGroup(index, direction) {
      const newIndex = index + direction
      try {
        await axios.put('/api/settings/product-groups/reorder', {
          id: this.groups[index].id,
          newOrder: this.groups[newIndex].order
        })
        this.fetchGroups()
      } catch (error) {
        this.$message.error('移动失败')
      }
    },
    addProduct() {
      this.productDialog.form = { code: '', name: '', min_amount: 0 }
      this.productDialog.visible = true
    },
    async saveProduct() {
      try {
        await axios.post(`/api/settings/product-groups/${this.selectedGroup.id}/products`, 
          this.productDialog.form)
        this.productDialog.visible = false
        this.fetchProducts()
        this.$message.success('添加成功')
      } catch (error) {
        this.$message.error('添加失败')
      }
    },
    async updateProduct(product) {
      try {
        await axios.put(`/api/settings/products/${product.id}`, product)
        this.$message.success('更新成功')
      } catch (error) {
        this.$message.error('更新失败')
      }
    },
    async deleteProduct(product) {
      try {
        await this.$confirm('确认删除该产品?', '提示', {
          type: 'warning'
        })
        await axios.delete(`/api/settings/products/${product.id}`)
        this.fetchProducts()
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    }
  }
}
</script>

<style scoped>
.product-groups {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 